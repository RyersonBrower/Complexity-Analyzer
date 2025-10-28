import subprocess, time, requests

def test_dockerized_app_responds():
    container_name = "complexity-analyzer-test"
    host_port = 5003  # change this if needed

    # Build and run your container using the Dockerfile in /analyzer
    subprocess.run(["docker", "build", "-t", "complexity-analyzer", "analyzer"], check=True)
    subprocess.run(["docker", "run", "-d", "-p", f"{host_port}:5000", "--name", container_name, "complexity-analyzer"], check=True)

    # Wait for Flask to start
    time.sleep(10)

    # Send a test request to the mapped host port
    resp = requests.post(f"http://localhost:{host_port}/analyze", json={"code": "for i in range(n): pass"})
    assert resp.status_code == 200
    assert "big_o_hint" in resp.json()

    # Clean up
    subprocess.run(["docker", "stop", container_name])
    subprocess.run(["docker", "rm", container_name])
