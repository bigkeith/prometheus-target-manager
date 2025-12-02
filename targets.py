from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)
TARGETS_FILE = 'targets.json'

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
        <h2>Current Hosts</h2>
        <ul>
        {% for host in data[0].targets %}
            <li>{{ host }}</li>
        {% endfor %}
        </ul>

        <h3>Add Host</h3>
        <form method="post">
            Server Name: <input type="text" name="server"><br>
            Port: <input type="text" name="port"><br>
            <input type="submit" name="add_host" value="Add Host">
        </form>

        <h3>Remove Host</h3>
        <form method="post">
            Host to Remove (e.g. host1.com:60443): <input type="text" name="remove_server"><br>
            <input type="submit" name="remove_host" value="Remove Host">
        </form>

        <p><strong>{{ message }}</strong></p>
    ''', data=data, message=message)

if __name__ == '__main__':
    app.run(debug=True)