from time import sleep, time
from subprocess import *
import re

default_dir = '.'

def monitor_qlen(iface, interval_sec = 0.01, fname='%s/qlen.txt' % default_dir, host=None):
    pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
    cmd = "tc -s qdisc show dev %s" % (iface)
    # monitoring is run on host if provided
    runner = Popen if host is None else host.popen

    ret = []
    open(fname, 'w').write('')
    while 1:
        p = runner(cmd, shell=True, stdout=PIPE)
        output = p.stdout.read()
        # Not quite right, but will do for now
        matches = pat_queued.findall(output)
        if matches and len(matches) > 1:
            ret.append(matches[1])
            t = "%f" % time()
            open(fname, 'a').write(t + ',' + matches[1] + '\n')
        sleep(interval_sec)
    return


def monitor_devs_ng(fname="%s/txrate.txt" % default_dir, interval_sec=0.01):
    """Uses bwm-ng tool to collect iface tx rate stats.  Very reliable."""
    cmd = ("sleep 1; bwm-ng -t %s -o csv "
           "-u bits -T rate -C ',' > %s" %
           (interval_sec * 1000, fname))
    Popen(cmd, shell=True).wait()


def monitor_bbr(dst, interval_sec = 0.01, fname='%s/bbr.txt' % default_dir, host=None):
    cmd = "ss -iet dst %s" % (dst)
    runner = Popen if host is None else host.popen
    print dst
    ret = []
    open(fname, 'w').write('')
    while 1:
        p = runner(cmd, shell=True, stdout=PIPE)
        output = p.stdout.read()
        try:
            start = output.find("bbr:(")
            end = output.find(")", start)
            if start == -1 or end == -1:
                continue
            data_elems = output[start+5:end].split(",")
            data = {}
            for d in data_elems:
                k, v = d.split(":")
                data[k] = v
            csvformat = "%s, %s, %s, %s" % (
                data["bw"],
                data["mrtt"],
                data["pacing_gain"],
                data["cwnd_gain"]
            )
            open(fname, 'a').write(csvformat + "\n")
        except Exception:
            pass
        sleep(interval_sec)
    return
