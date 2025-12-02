from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)
TARGETS_FILE = '/app/files/targets.json'

# Ensure targets.json exists with original structure
if not os.path.exists(TARGETS_FILE):
    with open(TARGETS_FILE, 'w') as f:
        json.dump([{
            "targets": [],
            "labels": {
                "job": "node",
                "servers": "managed"
            }
        }], f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    with open(TARGETS_FILE, 'r') as f:
        data = json.load(f)

    if request.method == 'POST':
        # Add Host
        if 'add_host' in request.form:
            server = request.form.get('server')
            port = request.form.get('port')
            if server and port:
                new_host = f"{server}:{port}"
                if new_host not in data[0]["targets"]:
                    data[0]["targets"].append(new_host)
                    message = f"✅ Added {new_host}"
                else:
                    message = f"⚠️ Host {new_host} already exists"
                with open(TARGETS_FILE, 'w') as f:
                    json.dump(data, f, indent=2)

        # Remove Host
        elif 'remove_host' in request.form:
            host_to_remove = request.form.get('remove_server')
            if host_to_remove in data[0]["targets"]:
                data[0]["targets"].remove(host_to_remove)
                message = f"✅ Removed {host_to_remove}"
            else:
                message = f"⚠️ Host {host_to_remove} not found"
            with open(TARGETS_FILE, 'w') as f:
                json.dump(data, f, indent=2)

    return render_template_string('''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Prometheus Targets Manager</title>
    https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="mb-4">Prometheus Targets Manager</h1>

    {% if message %}
    <div class="alert alert-info">{{ message }}</div>
    {% endif %}

    <div class="card mb-4">
        <div class="card-header">Current Hosts</div>
        <div class="card-body">
            {% if data[0].targets %}
            <ul class="list-group">
                {% for host in data[0].targets %}
                <li class="list-group-item">{{ host }}</li>
                {% endfor %}
            </ul>
            {% else %}
            <p>No hosts configured yet.</p>
            {% endif %}
        </div>
    </div>

    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">Add Host</div>
                <div class="card-body">
                    <form method="post">
                        <div class="mb-3">
                            <label class="form-label">Server Name</label>
                            <input type="text" name="server" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Port</label>
                            <input type="text" name="port" class="form-control" required>
                        </div>
                        <button type="submit" name="add_host" class="btn btn-primary">Add Host</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">Remove Host</div>
                <div class="card-body">
                    <form method="post">
                        <div class="mb-3">
                            <label class="form-label">Host to Remove (e.g. host1.com:60443)</label>
                            <input type="text" name="remove_server" class="form-control" required>
                        </div>
                        <button type="submit" name="remove_host" class="btn btn-danger">Remove Host</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
    ''', data=data, message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)