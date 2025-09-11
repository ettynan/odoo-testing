# Team Onboarding – Remote SSH + Odoo Tests

This guide explains how to join the Odoo testing droplet with full VS Code + Docker access.  

---

## A) Admin Tasks (done once per teammate)

### 1. Create a Linux user
```bash
adduser chris
usermod -aG sudo chris
usermod -aG docker chris
```

### 2. Add their SSH public key
```bash
mkdir -p /home/chris/.ssh
nano /home/chris/.ssh/authorized_keys    # paste contents of id-do.pub
chown -R chris:chris /home/chris/.ssh
chmod 700 /home/chris/.ssh
chmod 600 /home/chris/.ssh/authorized_keys
```

### 3. Give access to Odoo addons
```bash
chmod 755 /opt /opt/odoo-docker /opt/odoo-docker/addons
```

### 4. Optional shortcuts
```bash
ln -s /opt/odoo-docker/addons/om_hospital /home/chris/om_hospital
ln -s /opt/odoo-docker/addons/fleet_ext_tests /home/chris/fleet_tests
chown -h chris:chris /home/chris/om_hospital /home/chris/fleet_tests
```

---

## B) Teammate Setup (on their own laptop)

### 1. Generate SSH key
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id-do -C id-do
```
Send `~/.ssh/id-do.pub` to the admin.

### 2. Configure SSH
Add to `~/.ssh/config`:
```
Host odoo-droplet-chris
    HostName YOUR_DROPLET_IP
    User chris
    IdentityFile ~/.ssh/id-do
```

### 3. Test connection
```bash
ssh odoo-droplet-chris
groups   # should show: chris sudo docker
```

---

## C) VS Code Setup

1. Install extension: **Remote - SSH**.  
2. Connect: click green `><` in bottom-left → **Connect to Host…** → `odoo-droplet-chris`.  
3. Open folders:
   - `/opt/odoo-docker/addons/om_hospital`  
   - `/opt/odoo-docker/addons/fleet_ext_tests`  
   (Tip: use **Add Folder to Workspace…** to see both at once.)  
4. Open a terminal in VS Code → run Docker commands.

---

## D) Running Tests

### Fleet
```bash
sudo docker exec -it odoo-docker-odoo-1 odoo   --stop-after-init --no-http --workers=0   -d odoo_ut_fleet -u fleet_ext_tests   --without-demo=all --test-tags /fleet_ext_tests   --log-level=error --log-handler=odoo.tests:INFO
```

### om_hospital
```bash
sudo docker exec -it odoo-docker-odoo-1 odoo   --stop-after-init --no-http --workers=0   -d odoo_ut_hospital -u om_hospital   --without-demo=all --test-tags /om_hospital   --log-level=error --log-handler=odoo.tests:INFO
```

### Run a single Fleet test method
```bash
sudo docker exec -it odoo-docker-odoo-1 odoo   --stop-after-init --no-http --workers=0   -d odoo_ut_fleet -u fleet_ext_tests   --without-demo=all   --test-tags /fleet_ext_tests/test_fleet_basic:TestFleetExternal:test_odometer_log   --log-level=error --log-handler=odoo.tests:INFO
```

---

## E) Scaffold Missing Test Folders (if needed)

**om_hospital:**
```bash
mkdir -p /opt/odoo-docker/addons/om_hospital/tests
touch /opt/odoo-docker/addons/om_hospital/tests/__init__.py
```

**fleet_ext_tests:**  
Already exists with:
```
/opt/odoo-docker/addons/fleet_ext_tests/tests/test_fleet_basic.py
```

---

## F) Notes

- All files saved in VS Code → Remote SSH **stay on the droplet**.  
- Docker access requires `docker` group; if denied, log out and back in.  
- Explorer only shows what you open; use **multi-root workspace** for both hospital + fleet.  
- Admin can revoke access anytime by removing the user from `/etc/passwd` and deleting `/home/username`.

---
 
