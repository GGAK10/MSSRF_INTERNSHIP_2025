from flask import Flask, render_template_string
import subprocess
import webbrowser

app = Flask(__name__)

LOGO_URL = "https://th.bing.com/th/id/R.a0f8aedac2cfc7d2a0da03219b2e7553?rik=YZzehv8WyFdJlA&riu=http%3a%2f%2fintranet.mssrf.res.in%2fsites%2fdefault%2ffiles%2f2020mssrflogo.png&ehk=VGpf9Aui1eoJmNTNwkubwp659wLe0jHfy6HIoqSH7h4%3d&risl=&pid=ImgRaw&r=0"

HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GIS Tools - MSSRF</title>
    <style>
        html, body {{
            height: 100%;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?auto=format&fit=crop&w=1470&q=80');
            background-size: cover;
            background-position: center;
            color: #333;
        }}
        header {{
            background-color: rgba(255, 255, 255, 0.90);
            padding: 10px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        header .logo img {{
            height: 70px;
        }}
        nav {{
            display: flex;
            gap: 10px;
        }}
        nav a button {{
            background-color: #6c757d;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
            transition: transform 0.3s ease, background-color 0.3s ease;
        }}
        nav a button:hover {{
            background-color: #343a40;
            transform: scale(1.05);
        }}
        main {{
            flex: 1;
            display: flex;
            justify-content: space-between;
            padding: 40px;
        }}
        .main-panel {{
            background-color: rgba(255, 255, 255, 0.75);  /* Reduced opacity for more transparency */
            border-radius: 10px;
            padding: 30px;
            width: 45%;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .main-panel h1 {{
            font-size: 20px;
            margin-bottom: 25px;
            color: #1a1a1a;
        }}
        form {{
            margin: 15px 0;
        }}
        form button {{
            padding: 12px 24px;
            font-size: 16px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        form button:hover {{
            background-color: #0056b3;
        }}
        .info-panel {{
            width: 50%;
            background-color: rgba(255, 255, 255, 0.75);  /* More transparent for the right panel */
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            overflow-y: auto;
            max-height: 600px;
        }}
        .info-section {{
            display: none;
            animation: fadeIn 0.5s ease-in-out;
        }}
        .info-section.active {{
            display: block;
        }}
        .info-section h3 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #007BFF;
        }}
        .info-section p {{
            font-size: 15px;
            line-height: 1.6;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        footer {{
            background-color: #222;
            color: #ccc;
            text-align: center;
            padding: 15px;
            font-size: 14px;
        }}
    </style>
    <script>
        function showSection(id) {{
            const sections = document.querySelectorAll('.info-section');
            sections.forEach(sec => sec.classList.remove('active'));

            const buttons = document.querySelectorAll('nav a button');
            buttons.forEach(btn => btn.classList.remove('active'));

            document.getElementById(id).classList.add('active');
            const activeBtn = document.getElementById(id + '-btn');
            if (activeBtn) activeBtn.classList.add('active');
        }}
        window.onload = function() {{
            showSection('about');
        }}
    </script>
</head>
<body>
    <header>
        <div class="logo">
            <a href="https://development.mssrf.org/" target="_blank">
                <img src="{LOGO_URL}" alt="MSSRF Logo">
            </a>
        </div>
        <nav>
            <a href="https://development.mssrf.org/" target="_blank"><button>Home</button></a>
            <a href="#!" onclick="showSection('about')"><button id="about-btn">About</button></a>
            <a href="#!" onclick="showSection('problem')"><button id="problem-btn">Research Problem</button></a>
            <a href="#!" onclick="showSection('gap')"><button id="gap-btn">Research Gap</button></a>
            <a href="#!" onclick="showSection('methodology')"><button id="methodology-btn">Methodology</button></a>
            <a href="#!" onclick="showSection('tools')"><button id="tools-btn">Varied Tools</button></a>
        </nav>
    </header>
    <main>
        <div class="main-panel">
            <h1>A Standalone GIS & Remote Sensing Tool - Automation of LULC Classification using Machine Learning</h1>
            <form action="/run_script1" method="post">
                <button type="submit">Draw ROI</button>
            </form>
            <form action="/run_script2" method="post">
                <button type="submit">Upload Shape File</button>
            </form>
        </div>
        <div class="info-panel">
            <div id="about" class="info-section">
                <h3>About</h3>
                <p>
                    This tool empowers users to extract high-resolution satellite imagery with up to <strong>10-meter spatial resolution</strong>, enabling precise analysis of specific regions of interest. 
                    It supports <strong>Land Use and Land Cover (LULC) classification</strong> and delivers high accuracy in identifying and mapping different landscape features for research and monitoring purposes.
                </p>
            </div>
            <div id="problem" class="info-section">
                <h3>Research Problem</h3>
                <p>
                    There is a need for efficient tools that simplify the extraction and classification of satellite imagery while delivering actionable insights in real-time. 
                    Current platforms often lack integration and user-friendliness, making geospatial workflows cumbersome.
                </p>
            </div>
            <div id="gap" class="info-section">
                <h3>Research Gap</h3>
                <p>
                    Many existing geospatial tools do not effectively bridge the gap between advanced analytics and field usability. 
                    This platform addresses that void by combining high-resolution processing with a simple user interface, improving both accessibility and performance.
                </p>
            </div>
            <div id="methodology" class="info-section">
                <h3>Methodology</h3>
                <p>
                    The workflow incorporates <strong>Object-Based Image Analysis (OBIA)</strong>, supervised classification methods, and integration of <strong>shapefiles</strong> to analyze satellite imagery and generate region-specific insights. 
                    This approach ensures scalability and customization for diverse applications.
                </p>
            </div>
            <div id="tools" class="info-section">
                <h3>Varied Tools</h3>
                <p>
                    This project integrates <strong>Python</strong>, <strong>Flask</strong>, and <strong>Google Earth Engine</strong> for remote sensing and spatial data processing. 
                    Dataset include Sentinel-2, and user-defined shapefiles to facilitate advanced geospatial analysis.
                </p>
            </div>
        </div>
    </main>
    <footer>
        Copyright &copy; GIS and Remote Sensing Team | MSSRF 2025. All Rights Reserved.
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.post('/run_script1')
def run_script1():
    subprocess.Popen(["python", "D:/INTERNSHIP_MSSRF_2025/Satellite_data/Final_python/ROI_Draw_Download_Final_01.py"])
    return "*********** RUNNING and REDIRECTING to LOCAL HOST With PORT →  http://localhost:5005 ***********"

@app.post('/run_script2')
def run_script2():
    subprocess.Popen(["python", "D:/INTERNSHIP_MSSRF_2025/Satellite_data/Final_python/Upload_Download_Final_01.py"])
    return "*********** RUNNING and REDIRECTING to LOCAL HOST With PORT →  http://localhost:5004 ***********"

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(port=5000)
