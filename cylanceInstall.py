#!/usr/bin/env python
#
# written by brady
#version 0.1


import platform, time, os, sys

osVers = platform.platform()
hostName = platform.node()

# Function to get RedHat OS version to pick the correct install package
def osVersion(osVers):
    print('----------------------------------------------------')
    print('[-] Checking host platform and version for compatibility...')
    print('----------------------------------------------------')
    time.sleep(2)
    if('el5' in osVers):
        print('----------------------------------------------------')
        print('[!] Failed! This is RHEL 5 and is NOT compatible!')
        exit(0)
    elif('el6' in osVers):
        print('----------------------------------------------------')
        print('[+] Passed! This is RHEL 6')
        time.sleep(2)
        rpmVers = 'el6'
        return(rpmVers)
    elif('el7' in osVers):
        print('----------------------------------------------------')
        print('[+] Passed! This is RHEL 7')
        time.sleep(2)
        rpmVers = 'el7'
        return(rpmVers)
    else:
        print('----------------------------------------------------')
        print('''FAILED! Version of OS is not compatible with this script.
This platform is %s''') % (osVers)
        exit(0)

# This function doesn't really matter in this script, but keeping it to remove any noncompat version.
def getBit(osVers):
    if('x86_64' in osVers):
        print('------------------------------')
        print('[+] This Linux is 64 bit')
        bitVers = 'x86_64'
        return(bitVers)
    elif('i386' in osVers):
        print('------------------------------')
        print('[+] This Linux is i386')
        bitVers = 'i386'
        # Maybe I should exit here?
        return(bitVers)
    elif('i686' in osVers):
        print('------------------------------')
        print('[+] This Linux is i686')
        bitVers = 'i386'
        # Maybe I should exit here?
        return(bitVers)
    else:
        print('----------------------------------------------------')
        print('''FAILED! Version of OS is not compatible with this script.
This platform is %s''') % (osVers)
        exit(0)

#Function to delete old directory if found, but only after uninstalling old version in another function
def cleanup(dirName):
    cleanCmd = '/bin/rm -rf %s' % dirName
    cleanRun = os.popen(cleanCmd)
    cleanResult = str(cleanRun.read())
    print(cleanResult)

#Function calls cleanup function... if needed and then installs new package.
#Gets complete package from satellite server, includes el6 and el7 rpms and config_defaults.txt
#Also, note during unzip it will place the config_defaults.txt in the new install directory
def installAgent(pkgName, rpmName):
    print('[+] Getting new version from Satellite and installing...')
    dirName = '/opt/cylance/'
    if os.path.exists(dirName):
        print('[!] Found Old Cylance directory, cleaning up first.')
        cleanup(dirName)
        time.sleep(3)

    workingDir = os.mkdir(dirName)
    get = '/usr/bin/wget --no-check-certificate --no-proxy http://###.###.###.###/pub/%s' % pkgName
    getRun = os.popen(get)
    getResult = str(getRun.read())
    extractPkg = '/usr/bin/unzip -d %s %s' % (dirName, pkgName)
    print('[+] Extracting...')
    pkgExtract = os.popen(extractPkg)
    time.sleep(2)
    extractResult = str(pkgExtract.read())
    print(extractResult)
    installRPM = '/usr/bin/yum -y %s%s' % (dirName, rpmName)
    print('[+] Installing...')
    rpmInstall = os.popen(installRPM)
    time.sleep(2)
    installResult = str(rpmInstall.read())
    print(installResult)
    cleanup(dirName)

#Function that checks for current version, ALWAYS make sure the current version is updated in the `agentVers` variable!!!!!
#If Cylance is installed and it is an older version it will be removed! 
#Maybe add a user input here to double check?
def chkPkg(rpmVers):
    agentVers = '2.0.1500-316'
    pkgName = 'CylancePROTECT.zip'
    rpmName = 'CylancePROTECT.%s.rpm' % (rpmVers)
    print('[-] Checking what version of Cylance is installed...')
    checkRPM = '/bin/rpm -qa | grep -i cylance | grep -v grep'
    runCheckRPM = os.popen(checkRPM)
    time.sleep(3)
    rpmResult = str(runCheckRPM.read())
    #Double sanity 
    if('Cylance' in rpmResult):
        if(agentVers in rpmResult):
            print('[+] CylancePROTECT is already installed with current version')
            sys.exit(0)
        else:
            print('[+] CylancePROTECT agent is installed with older version')
            removeRPM = '/bin/rpm -e %s' % rpmResult
            print('[-] Removing older version of CylancePROTECT %s') % rpmResult
            rpmRemove = os.popen(removeRPM)
            time.sleep(3)
            removeResult = str(rpmRemove.read())
            print(removeResult)
            installAgent(pkgName, rpmName)
    else:
        print('[+] No version of CylancePROTECT found installed...installing')
        installAgent(pkgName, rpmName)

checkTrend = '/bin/rpm -qa | grep -i ds_agent | grep -v grep'
runCheckTrend = os.popen(checkTrend)
time.sleep(3)
trendResult = str(runCheckTrend.read())
#Double sanity 
if('ds_agent' in trendResult):
    print('[+] TrendMicro agent is installed and needs to be removed')
    removeTrend = '/bin/rpm -e %s' % trendResult
    print('[-] Removing older version of CylancePROTECT %s') % trendResult
    trendRemove = os.popen(removeTrend)
    time.sleep(3)
    removeTrendResult = str(trendRemove.read())
    print(removeTrendResult)
    time.sleep(3)
    rpmVers = osVersion(osVers)
    # Sanity check only
    bitVers = getBit(osVers)
    chkPkg(rpmVers)
else:
    print('[+] TrendMicro is not found on this system! Move forward!')
    time.sleep(3)
    rpmVers = osVersion(osVers)
    # Sanity check only
    bitVers = getBit(osVers)
    chkPkg(rpmVers)
