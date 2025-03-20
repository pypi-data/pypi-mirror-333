# ✨ Welcome to CosmoTalker v1.4 - Your Gateway to the Cosmos!

🚀 **CosmoTalker v1.4** is here! Explore space and science effortlessly with this offline Python library, now with an enhanced deep search function and a new feedback feature.

## 🌠 About CosmoTalker

Developed by **Bhuvanesh M**, CosmoTalker is a Python library that brings knowledge of celestial bodies, scientific phenomena, and space-related information directly to your system—no internet required for core data! However, enhanced search and up-to-date space-related news require an internet connection.

## ✨ Features:

✅ Get detailed information about celestial bodies within the **Solar System** 🌍☀️\
✅ Learn about various scientific phenomena 🔬\
✅ Ask space and science-related questions for insightful responses 🧑‍🔬\
✅ Works **offline** with the new Python module 🖥️🚀\
✅ Optional **online** features for enhanced exploration 🌌

✅ **New!** `cosmotalker.feedback()`: Now you can provide feedback to improve CosmoTalker! 💡

📡 **Note:** CosmoTalker v1.0 focused on the **Solar System**. Future updates will expand its capabilities to explore galaxies and beyond! ✨

## 🌍 Contribute to a Greener Planet!

The 'Search on Web' feature, available at [bhuvaneshm.in/cosmotalker](https://bhuvaneshm.in/cosmotalker) and as the `cosmotalker.search(str)` function in the Python library (since v1.1.1), supports a greener Earth by using the Ecosia search engine 🌱💚. Every search helps plant trees and contribute to reforestation 🌳. This function requires a string input and performs an online search.

## 🛠 Installation & Usage

### Installation:

```sh
pip install cosmotalker
```

### Basic Usage:

```python
import cosmotalker as ct

# Retrieve information about a celestial body
earth_info = ct.get("earth")
print(earth_info)  # Offline function

# Provide feedback to improve CosmoTalker
ct.feedback()

# Online Features
print(ct.apod())        # Fetch Astronomy Picture of the Day
print(ct.celestrak())   # Get satellite tracking data
print(ct.search("words"))  # Eco-friendly web search with Ecosia
print(ct.search("yt"))  # Opens YouTube
print(ct.get("yuri"))  # Deep search about Yuri
```

📌 **Note:** In `ct.search()`, you can use shortcuts like `wa` for WhatsApp, `fb` for Facebook, `insta` for Instagram, `gpt` for ChatGPT, etc., or provide a query to perform an online search.

## 🔥 Benchmark Performance

CosmoTalker's core data is stored offline, ensuring lightning-fast retrieval speeds without network latency. Here are some benchmark results (measured in seconds):

```
0.000781298
0.000829697
0.018242359
0.000800371
0.000974417
0.000877857
0.000807524
0.000780582
0.000797749
```

## 🌌 Explore More

Visit **[bhuvaneshm.in/cosmotalker](https://bhuvaneshm.in/cosmotalker)** to discover more about the universe!

---

👨‍💻 **Developed by** [Bhuvanesh M](https://github.com/bhuvanesh-m-dev)

### 🌐 Connect with Me:

- **Portfolio**: [bhuvaneshm.in](https://bhuvaneshm.in/)
- **LinkedIn**: [linkedin.com/in/bhuvaneshm-developer](https://www.linkedin.com/in/bhuvaneshm-developer)
- **GitHub**: [github.com/bhuvanesh-m-dev](https://github.com/bhuvanesh-m-dev)
- **HackerRank**: [hackerrank.com/profile/bhuvaneshm\_dev](https://www.hackerrank.com/profile/bhuvaneshm_dev)
- **YouTube**: [youtube.com/@bhuvaneshm\_dev](https://www.youtube.com/@bhuvaneshm_dev)
- **LeetCode**: [leetcode.com/u/bhuvaneshm\_dev](https://leetcode.com/u/bhuvaneshm_dev/)
- **X (Twitter)**: [x.com/bhuvaneshm06](https://x.com/bhuvaneshm06)
- **Instagram**: [instagram.com/bhuvaneshm.developer](https://www.instagram.com/bhuvaneshm.developer)


