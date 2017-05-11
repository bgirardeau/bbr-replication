# Setup

Modified from https://github.com/google/bbr/blob/master/Documentation/bbr-quick-start.md

```
typeset -x PROJECT="bbr-replication"  # An existing GCE project name
typeset -x ZONE="us-west1-a"          # Any GCE Zone
gcloud compute instances create "bbrtest1" \
    --project ${PROJECT} \
    --zone ${ZONE} \
    --machine-type "n1-standard-8" \
    --network "default" \
    --maintenance-policy "MIGRATE" \
    --boot-disk-type "pd-standard" \
    --boot-disk-device-name "bbrtest1" \
    --image "https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-1604-xenial-v20170502" \
    --boot-disk-size "20" \
    --scopes default="https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly"
gcloud compute ssh --project ${PROJECT} --zone ${ZONE} bbrtest1
sudo apt-get update
sudo apt-get build-dep linux
sudo apt-get upgrade
wget kernel.ubuntu.com/~kernel-ppa/mainline/v4.9/linux-headers-4.9.0-040900_4.9.0-040900.201612111631_all.deb
wget kernel.ubuntu.com/~kernel-ppa/mainline/v4.9/linux-headers-4.9.0-040900-generic_4.9.0-040900.201612111631_i386.deb
wget kernel.ubuntu.com/~kernel-ppa/mainline/v4.9/linux-image-4.9.0-040900-generic_4.9.0-040900.201612111631_i386.deb
sudo dpkg -i linux-headers-4.9.0*.deb linux-image-4.9.0*.deb
sudo reboot
sudo -i
echo "bbr" > /proc/sys/net/ipv4/tcp_congestion_control
exit
cat /proc/sys/net/ipv4/tcp_congestion_control
```

Install Mininet from Source 
git clone git://github.com/mininet/mininet 
cd mininet
git tag
git checkout -b 2.2.1 2.2.1 
cd ..
mininet/util/install.sh -a
