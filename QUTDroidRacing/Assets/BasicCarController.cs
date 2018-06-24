using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Net.Sockets;
using System.Text;
using System;


public class BasicCarController : MonoBehaviour {
	public System.Net.Sockets.TcpClient clientSocket;
	public NetworkStream stream;
	public string host = "localhost";
	public int port = 8005;

	public string STX = "METR";
	public string ETX = "BBL";
	public string messageString;
	public string buffer = "";
	public string[] messageData;
	public int watchdog = 0;

	public Transform frontLeftWheel;
	public Transform frontRightWheel;
	public Transform rearLeftWheel;
	public Transform rearRightWheel;

	public Transform car;

	public float vX = 0.0f;
	public float vY = 0.0f;
	public float theta = 0.0f;
	public float vTheta = 0.0f;
	public float vSteeringAngle = 0.0f;
	public float steeringAngle = 0.0f;
	public float targetSteeringAngle = 0.0f;
	public float steeringAngleGain = 0.2f;
	public float v = 0.0f;

	public float rideHeight = 0.5f;
	public float wheelRadius = 0.5f;
	public float wheelBase;

	public float telemetryFrequency = 10.0f;


	public float maxSteeringAngle = 45.0f;

	// Use this for initialization
	void Start () {
		clientSocket = new System.Net.Sockets.TcpClient ();
		clientSocket.Connect (host, port);
		stream = clientSocket.GetStream ();

		wheelBase = frontLeftWheel.localPosition.z - rearLeftWheel.localPosition.z;
		//car.position = new Vector3 (0.0f, rideHeight, 0.0f);
		//car.eulerAngles = new Vector3 (0.0f, theta, 0.0f);
		StartCoroutine (send_telemetry());
	}
	
	// Update is called once per frame
	void Update () {
		if (clientSocket.Available > 0) {
			watchdog++;
			Byte[] data = new Byte[256];
			Int32 bytes = stream.Read (data, 0, data.Length);
			buffer += System.Text.Encoding.ASCII.GetString (data, 0, bytes);
			while (true) {
				int stxPos = buffer.IndexOf (STX);
				int etxPos = buffer.IndexOf (ETX);
				if (etxPos < stxPos) {
					buffer = buffer.Substring (stxPos, buffer.Length - stxPos - STX.Length);
				} else if (stxPos != -1 && stxPos != -1) {
					messageString = buffer.Substring (stxPos + STX.Length, etxPos - stxPos - STX.Length);
					buffer = buffer.Substring (etxPos + ETX.Length, buffer.Length - etxPos - ETX.Length);
					messageData = messageString.Split (',');

					process_input ();

				} else {

					break;
				}
			}
		}

		update_car ();
	}

	IEnumerator send_telemetry() {
		while (true) {

			yield return new WaitForSeconds (1.0f / telemetryFrequency);

			byte[] telemetry = new byte[sizeof(float) * 5];
			byte[] floatBytes = new byte[sizeof(float)];

			float[] floats = new float[5];
			floats[0] = car.eulerAngles.y;
			floats[1] = car.position.x;
			floats[2] = car.position.z;
			floats [3] = v;
			floats [4] = steeringAngle;


			for (int i = 0; i < 5; i++) {
				floatBytes = System.BitConverter.GetBytes (floats [i]);
				for (int j = 0; j < sizeof(float); j++) {
					telemetry [sizeof(float) * i + j] = floatBytes [j];
				}
			}

			stream.Write (System.Text.Encoding.UTF8.GetBytes(STX), 0, STX.Length);
			stream.Write (telemetry, 0, sizeof(float) * 5);
			stream.Write (System.Text.Encoding.UTF8.GetBytes(ETX), 0, ETX.Length);
			yield return null;
		}
	}

	void process_input() {
		v = float.Parse(messageData [0]);
		targetSteeringAngle = float.Parse(messageData [1]);
		Debug.Log (targetSteeringAngle);	
		if (targetSteeringAngle > maxSteeringAngle) {
			targetSteeringAngle = maxSteeringAngle;
		} else if (targetSteeringAngle < -maxSteeringAngle) {
			targetSteeringAngle = -maxSteeringAngle;
		}
		//steeringAngle = targetSteeringAngle;
	}

	void update_car() {
		float dt = Time.deltaTime;
		vX = Mathf.Cos (Mathf.Deg2Rad*theta) * v;
		vY = Mathf.Sin (Mathf.Deg2Rad*theta) * v;
		vTheta = v * Mathf.Tan (Mathf.Deg2Rad*steeringAngle) / wheelBase / Mathf.Deg2Rad;
		//vSteeringAngle = vSteeringAngle;

		steeringAngle += (targetSteeringAngle - steeringAngle) *steeringAngleGain* dt;
		Vector3 currentPos = car.position;
		car.position = new Vector3 (currentPos.x + vY * dt, rideHeight, currentPos.z + vX * dt);
		theta = theta + dt * vTheta;
		car.eulerAngles = new Vector3 (0.0f, theta, 0.0f);

		float wheelAngle = frontLeftWheel.localEulerAngles.x + dt * v / Mathf.Deg2Rad / wheelRadius;
		frontLeftWheel.localEulerAngles = new Vector3 (wheelAngle, steeringAngle, 0.0f);
		wheelAngle = frontRightWheel.localEulerAngles.x + dt * v / Mathf.Deg2Rad / wheelRadius;
		frontRightWheel.localEulerAngles = new Vector3 (wheelAngle, steeringAngle, 0.0f);
		wheelAngle = rearLeftWheel.localEulerAngles.x + dt * v / Mathf.Deg2Rad / wheelRadius;
		rearLeftWheel.localEulerAngles = new Vector3 (wheelAngle, 0.0f, 0.0f);
		wheelAngle = rearRightWheel.localEulerAngles.x + dt * v / Mathf.Deg2Rad / wheelRadius;
		rearRightWheel.localEulerAngles = new Vector3 (wheelAngle, 0.0f, 0.0f);
	}
}

