from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/error')
def trigger_error():
    raise ValueError('This is a deliberate error')

# Updated HTML template with cleaner structure
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
    </style>
  </head>
  <body>
    <button id="startButton">Start</button>
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
        let currentIndex = 0;

        function startTimer(index) {
          let totalSeconds = timers[index][1] * 60 + timers[index][2];
          const timerElement = document.getElementById(`timer${index + 1}`);
          const containerElement = document.getElementById(`container${index + 1}`);
          containerElement.style.display = 'block';

          function updateTimer() {
            const minutes = Math.floor(totalSeconds / 60);
            const seconds = totalSeconds % 60;
            timerElement.innerText = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            if (totalSeconds > 0) {
              totalSeconds--;
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
