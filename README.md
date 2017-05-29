# Setup

Modified from https://github.com/google/bbr/blob/master/Documentation/bbr-quick-start.md
Create a new GCE project and a new VM Instance

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
    --boot-disk-size "30" \
    --scopes default="https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly"
```

Clone the experiment repository and install dependencies:

```
gcloud compute ssh --project ${PROJECT} --zone ${ZONE} bbrtest1
git clone https://github.com/bgirardeau/bbr-replication
cd bbr-replication
# This step will take ~10 minutes to download and install a modified linux kernel.
# You will occasionally have to press Y/enter to continue installation.
# At the end of this script, the vm will reboot, ending your ssh session.
sudo ./install1.sh
```

Finish Installations:
```
gcloud compute ssh --project ${PROJECT} --zone ${ZONE} bbrtest1
cd bbr-replication
sudo ./install2.sh
```

Run the experiments:
```
sudo ./figure5.sh
sudo ./figure6.sh
```
