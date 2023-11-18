<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
</head>

<body>
  <h1 align="center">NetworkDetective 🌐</h1>

  <p align="center">
      <a href="https://tryhackme.com/p/TxVScoobyDoo">
          <img src="https://tryhackme-badges.s3.amazonaws.com/TxVScoobyDoo.png" alt="TryHackMe Profile">
      </a>
  </p>

  <h2>About NetworkDetective</h2>

  <p>🚀 **NetworkDetective** is a powerful Python tool designed for network reconnaissance and security analysis. It provides essential features to scan active IPs, perform port scans, and inspect banners on open ports.</p>

  <h2>Features</h2>

  <ul>
      <li>🌐 Scan active IPs in a network</li>
      <li>🕵️ Perform port scans for detailed analysis</li>
      <li>🚪 Inspect banners on open ports</li>
      <li>📈 User-friendly interface with colorful progress bars</li>
      <li>🔄 Multithreading for efficient scanning</li>
  </ul>

  <h2>Getting Started</h2>

  <h3>Prerequisites</h3>

  <p>Make sure you have Python installed. You can install the required dependencies using:</p>

  <pre><code>pip install -r requirements.txt</code></pre>

  <h3>Usage</h3>

  <p>To run NetworkDetective, use the following command in the terminal:</p>

 <h2>Usage</h2>

<p>Command: <code>python networkDetective.py  [OPTION] [ARGUMENT]</code></p>

<table>
    <thead>
        <tr>
            <th>Option</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>-s, --scan &lt;NETWORK&gt;</code></td>
            <td>Check active IPs on a network</td>
        </tr>
        <tr>
            <td><code>-ps, --portscan &lt;IP&gt;</code></td>
            <td>Check open ports on an IP</td>
        </tr>
        <tr>
            <td><code>-mp, --maxport &lt;PORT&gt;</code></td>
            <td>Specify the maximum port for Port Scan</td>
        </tr>
        <tr>
            <td><code>-b, --banner &lt;IP&gt; &lt;PORT&gt;</code></td>
            <td>Check the banner on a specific port</td>
        </tr>
        <tr>
            <td><code>-v, --verbose</code></td>
            <td>Display detailed messages</td>
        </tr>
    </tbody>
</table>

<p>Examples:</p>

<pre>
<code>
# Check active IPs on a network
python networkDetective.py  -s 192.168.1.0

# Check open ports on an IP
python networkDetective.py  -ps 192.168.1.1

# Specify the maximum port for Port Scan
python networkDetective.py  -ps 192.168.1.1 -mp 100

# Check the banner on a specific port
python networkDetective.py  -b 192.168.1.1 80

# Display detailed messages
python networkDetective.py  -v
</code>
</pre>

</body>

</html>
