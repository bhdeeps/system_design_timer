from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello_world():
    home_page_html = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Home Page</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            padding: 20px;
          }
          h1 {
            font-size: 2em;
          }
          a {
            text-decoration: none;
            color: white;
            background-color: #007BFF;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1.2em;
          }
          a:hover {
            background-color: #0056b3;
          }
        </style>
      </head>
      <body>
        <h1>Welcome to the System Design Timer App!</h1>
        <p>Click the button below to access the system design timer:</p>
        <a href="/sequence">Go to System Design Timer</a>
      </body>
    </html>
    """
    return render_template_string(home_page_html)


@app.route('/error')
def trigger_error():
    raise ValueError('This is a deliberate error')

TIMER_SEQUENCE_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Sequence of Timers</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 20px;
      }
      .timer-container {
        margin-bottom: 20px;
        display: none;
      }
      h2 {
        font-size: 2em;
      }
      h3 {
        font-size: 1.5em;
        margin-top: 1em;
      }
      ul {
        padding-left: 20px;
      }
      .timer {
        font-size: 3em;
        margin-top: 10px;
      }
      #startButton {
        font-size: 1.5em;
        padding: 10px 20px;
        margin-bottom: 20px;
      }
      #overallTimer {
        font-size: 3em;
        margin-bottom: 20px;
        color: red;
      }
    </style>
  </head>
  <body>
    <button id="startButton">Start</button>
    
    <!-- Overall timer display -->
    <div id="overallTimer">Total Time: 0:00</div>

    {% for label, minutes, seconds, content in timers %}
      <div class="timer-container" id="container{{ loop.index }}">
        <h2>{{ label }}</h2>
        {{ content|safe }}
        <div id="timer{{ loop.index }}" class="timer">{{ minutes }}:{{ seconds }}</div>
      </div>
    {% endfor %}
    
    <script>
      document.getElementById('startButton').addEventListener('click', function() {
        const timers = {{ timers | tojson }};
        let totalSeconds = timers.reduce((acc, timer) => acc + (timer[1] * 60 + timer[2]), 0);
        let currentIndex = 0;

        // Display the overall timer
        const overallTimerElement = document.getElementById('overallTimer');

        function updateOverallTimer() {
          const minutes = Math.floor(totalSeconds / 60);
          const seconds = totalSeconds % 60;
          overallTimerElement.innerText = `Total Time: ${minutes}:${seconds.toString().padStart(2, '0')}`;
          if (totalSeconds > 0) {
            totalSeconds--;
            setTimeout(updateOverallTimer, 1000);
          }
        }
        
        // Start updating the overall timer
        updateOverallTimer();

        function startTimer(index) {
          let sectionTotalSeconds = timers[index][1] * 60 + timers[index][2];
          const timerElement = document.getElementById(`timer${index + 1}`);
          const containerElement = document.getElementById(`container${index + 1}`);
          containerElement.style.display = 'block';

          function updateTimer() {
            const minutes = Math.floor(sectionTotalSeconds / 60);
            const seconds = sectionTotalSeconds % 60;
            timerElement.innerText = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            if (sectionTotalSeconds > 0) {
              sectionTotalSeconds--;
              setTimeout(updateTimer, 1000);
            } else if (index < timers.length - 1) {
              containerElement.style.display = 'none';
              startTimer(index + 1);
            }
          }
          updateTimer();
        }

        startTimer(currentIndex);
        document.getElementById('startButton').style.display = 'none';
      });
    </script>
  </body>
</html>
"""


@app.route('/sequence')
def sequence():
    # Adding more detailed content for each page
    timers = [
        (
            "Requirements", 5, 0,
            """
            <h3>Functional</h3>
            <ul>
              <li>User and how it is used</li>
              <li>Photos and videos?</li>
              <li>Notifications?</li>
              <li>Security</li>
              <li>Compliance</li>
              <li>Existing company stack</li>
            </ul>
            <h3>Non-Functional</h3>
            <ul>
              <li>Fault tolerance</li>
              <li>Low latency (memory to batch processing times)</li>
              <li>Consistency (strong/eventual)</li>
              <li>Availability (high/low)</li>
              <li>Scalability (US population 400M)</li>
              <li>Reliability</li>
              <li>Durability</li>
              <li>ACID-ity</li>
              <li>Correctness</li>
              <li>Write/Read heavy</li>
            </ul>
            """
        ),
        (
            "Core entities and API/System interface (input and output) and data flow", 10, 0,
            """
            <h3>Core entities and API</h3>
            <ul>
              <li>APIs match every functional requirement</li>
              <li>Sample input params: api_dev_key (security), User_id, location, timestamp</li>
              <li>Return type: JSON or stream for video snippets</li>
              <li>For videos: codec, resolution, offset</li>
              <li>gRPC vs REST</li>
            </ul>
            """
        ),
        (
            "High-level design: functional requirements (API, Web/App servers, LB)", 10, 0,
            """
            <h3>High-level design</h3>
            <ul>
              <li>Match every API from the previous section</li>
              <li>Generic components: workers, CRUD service</li>
              <li>Client, API gateway, service, DB, synchronous flows</li>
            </ul>
            """
        ),
        (
            "Design deep dive (non-functional)", 25, 0,
            """
            <h3>Design deep dive</h3>
            <ul>
              <li>Fault tolerance and scaling (async flows, Kafka)</li>
              <li>Latency (caching, optimized DB, CDN)</li>
              <li>Scaling (sync to async, managed services, auto-scaling)</li>
              <li>Sharding DB, cache static content</li>
            </ul>
            """
        ),
        (
            "Wrap: (Bottleneck, metrics, alerts)", 5, 0,
            """
            <h3>Bottlenecks and Metrics</h3>
            <ul>
              <li>Bottlenecks (SPOD)</li>
              <li>System metrics (memory, I/O)</li>
              <li>Business metrics (#requests, success, failures)</li>
              <li>Prometheus, Grafana, Instana</li>
              <li>Alerts (ELK stack)</li>
            </ul>
            """
        )
    ]
    return render_template_string(TIMER_SEQUENCE_HTML, timers=timers)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
