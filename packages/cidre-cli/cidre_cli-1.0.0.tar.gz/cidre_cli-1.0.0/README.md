# 📡 CIDRE - CIDR Enhanced&#x20;

## ⚡ Quick Start

### **1️⃣ Install CIDRE**

```bash
pip install cidre-cli
```

### **2️⃣ Pull & Merge CIDR Ranges**

```bash
cidre pull --merge
```

- Downloads the latest CIDR allocations from RIRs.
- Merges overlapping IP ranges for efficiency.

### **3️⃣ Block Specific Countries in UFW**

```bash
cidre deny ru ir kp
```

- Blocks **Russia (RU), Iran (IR), and North Korea (KP)** in UFW.
- Requires **UFW installed** (`sudo apt install ufw`).

### **4️⃣ Allow Specific Countries in UFW**

```bash
cidre allow us gb de
```

- Allows **United States (US), United Kingdom (GB), and Germany (DE)** IPs in UFW.

### **5️⃣ Reject (Drop) Traffic from Specific Countries**

```bash
cidre reject cn ru
```

- Rejects (drops) traffic from **China (CN) and Russia (RU)**.

---

**CIDRE** is a CLI tool that **automatically pulls and compiles allocated IP ranges** from the five **Regional Internet Registries (RIRs)**:

- **AFRINIC** (Africa)
- **APNIC** (Asia-Pacific)
- **ARIN** (North America)
- **LACNIC** (Latin America & Caribbean)
- **RIPE NCC** (Europe, Middle East, Central Asia)

The fetched CIDR ranges are saved into:

```
./output/cidr/ipv4/{country}.cidr
./output/cidr/ipv6/{country}.cidr
```

By default, CIDRE stores files in `./output/cidr/`, but you can **override the storage location** using the `--store` argument.

Additionally, **CIDRE** can be used to **block entire countries' IPs in UFW (Uncomplicated Firewall)** on Linux.

📂 **All generated CIDR files are also available in this repository.**

---

## 🚀 Features

- **Daily automatic CIDR updates**.
- **Compiles CIDR blocks per country** from RIR allocation data.
- **Merges overlapping IP ranges** for efficiency.
- **Allows easy firewall rules** for blocking or allowing entire countries.
- **Supports both IPv4 & IPv6**.

---

## 🛠️ Installation

### **1️⃣ Install via PyPI**

```bash
pip install cidre-cli
```

### **2️⃣ Alternative: Clone the Repository**

```bash
git clone https://github.com/vulnebify/cidre.git
cd cidre-cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x cidre-cli.py
```

---

## ⚡ Usage

### **1️⃣ Pull and Compile CIDR Ranges**

Fetches the latest IP allocation data from all RIRs and **compiles per-country CIDR blocks**:

```bash
cidre pull --merge
```

- `--merge`: Merges overlapping IP ranges for efficiency.
- `--proxy`: Proxies connection to RIRs. 
- `--store <path>`: Specifies a custom storage directory.
- **Output Example:**
  - `output/cidr/ipv4/us.cidr` (United States IPv4 ranges)
  - `output/cidr/ipv6/de.cidr` (Germany IPv6 ranges)

### **2️⃣ Block Entire Countries with UFW**

Block specific countries' CIDR blocks in **UFW firewall**:

```bash
cidre deny ru ir kp
```

- Blocks **Russia (RU), Iran (IR), and North Korea (KP)** in the **Uncomplicated Firewall (UFW)**.
- Requires **UFW installed** (`sudo apt install ufw` on Debian/Ubuntu).

### **3️⃣ Allow Specific Countries**

```bash
cidre allow us gb de
```

- Allows **United States (US), United Kingdom (GB), and Germany (DE)** IPs in UFW.

### **4️⃣ Reject (Drop) Traffic from Specific Countries**

```bash
cidre reject cn ru
```

- Rejects (drops) traffic from **China (CN) and Russia (RU)**.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙌 Inspired By

CIDRE was inspired by **[herrbischoff/country-ip-blocks](https://github.com/herrbischoff/country-ip-blocks)** and aims to provide an automated alternative with firewall integration.

---

## 🤝 Contributions

PRs are welcome! Feel free to **fork the repo** and submit pull requests.

---

## 📧 Contact

For any questions, open an issue or reach out via GitHub Discussions.

