import argparse
import yaml
import os
import sys
import subprocess
import semver
import hashlib
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def _c(color, t):
    c = getattr(bcolors, color.upper())
    return "%s%s%s" % (c, t, bcolors.ENDC)

class Tag(object):
    def __init__(self, major, minor, patch, variant=None):
        self.major = major
        self.minor = minor 
        self.patch = patch
        self.variant = variant
    
    @classmethod
    def parse(cls, tag):
        comp = tag.split('-')
        version = comp[-1]
        variant = None
        if len(comp) > 1:
            variant = '-'.join(comp[:-1])
        t = version.split('.')
        if len(t) == 3:
            return cls(t[0],t[1],t[2], variant=variant)
        elif len(t) == 2:
            return cls(t[0],t[1],None, variant=variant)
        elif len(t) == 1:
            return cls(t[0],None,None, variant=variant)
        raise AssertionError('Unable to parse %s' % tag)

    def tags(self, build=None):
        parts = [self.major, self.minor, self.patch]
        tags = []
        tag = []
        for idx, pt in enumerate(parts):
            if pt is not None:
                tag.append(str(pt))
                if idx == 0:
                    continue
                if self.variant:
                    tags.append(self.variant + '-' + '.'.join(tag))
                    if idx == (len(parts) - 1):
                        if build is not None:
                            tags.append(self.variant + '-' + '.'.join(tag) + '-' + str(build))
                else:
                    tags.append('.'.join(tag))
                    if idx == (len(parts) - 1):
                        if build is not None:
                            tags.append('.'.join(tag) + '-' + str(build))
        return tags



def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--repofile', default='repo.yml')
    parser.add_argument('-p','--push', default=False, action='store_true')
    parser.add_argument('-c','--containerfile', default=None)
    parser.add_argument('-r','--release', default=False, action='store_true')
    parser.add_argument('--cmd', required=False, default='docker')
    parser.add_argument('directory')

    args = parser.parse_args()

    os.chdir(args.directory)   
    
    if args.containerfile is None:
        if os.path.exists('Containerfile'):
            containerfile = 'Containerfile'
        elif os.path.exists('Dockerfile'):
            containerfile = 'Dockerfile'
        else:
            print(_c('fail', 'Unable to locate Containerfile or Dockerfile'), file=sys.stderr)
            sys.exit(2)
    else:
        containerfile = args.containerfile
        if not os.path.exists(containerfile):
            print(_c('fail', 'Unable to locate %s' % containerfile), file=sys.stderr)
            sys.exit(2)
    
    if not os.path.exists(args.repofile):
        print(_c('fail', "%s not found, creating new" % args.repofile), file=sys.stderr)
        repo_url = input("Repo url (eg: docker.io/username/project): ")
        repo_tag = input("Version: (default: 0.1): ")
        if not repo_tag.strip():
            repo_tag = '0.1'
        with open(args.repofile, 'w') as rf:
            rf.write(f'repo: {repo_url}\n')
            rf.write(f'tag: {repo_tag}\n')
    
    with open(args.repofile, 'r') as f:
        conf = yaml.safe_load(f)
    
    repo = conf.get('repo', None)
    repos = conf.get('repos', [])
    target = conf.get('target', None)
    tag = str(conf['tag'])
    squash = conf.get('squash', None)
    
    stag = Tag.parse(tag)
    
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")
    utcnow = datetime.datetime.utcnow()
    build = (utcnow.hour * 60) + utcnow.minute
    
    build = '%s.%s' % (today, build)
    
    def build_image(args, stag, repo_url, target=None):

        tags = []   
        if args.release:
            for t in stag.tags(build):
                tags.append('%s:%s' % (repo_url, t))
            tags.append('%s:latest' % repo_url)
        else:
            tags.append('%s:development' % repo_url)
        
        print(_c('okblue', "+ Building %s" % repo_url))
        cmd = [args.cmd, 'build', '-f', containerfile]
        if squash:
            cmd += ['--squash']
        if target:
            cmd += ['--target', target]
        
        for t in tags:
            cmd += ['-t', t]
        cmd.append('.')
        
        out = subprocess.Popen(cmd).wait()
        if out != 0:
            raise ChildProcessError(' '.join(cmd))
        
        if args.push:
            for t in tags:
                print(_c('okblue', '+ Pushing %s' % t))
                cmd = [args.cmd, 'push', t]
                out = subprocess.Popen(cmd).wait()
                if out != 0:
                    raise ChildProcessError(' '.join(cmd))
            for t in tags:
                print(_c('okgreen', 'Pushed %s' % t))
        
    if repo:
        build_image(args, stag, repo, target)
    
    if repos:
        for r in repos:
            build_image(args, stag, r['url'], r.get('target', None))
    
    with open(args.repofile, 'w') as f:
        if args.release:
            conf['last_build'] = build
        yaml.safe_dump(conf, f)
