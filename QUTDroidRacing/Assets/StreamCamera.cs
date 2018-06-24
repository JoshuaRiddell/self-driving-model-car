using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
//using UnityEngine.Networking;
using UnityEngine.Windows;


public class StreamCamera : MonoBehaviour {

	public System.Net.Sockets.TcpListener server;
	public string host = "localhost";
	public int port = 8000;

	public Camera cam;
	public Transform car;
	public float framesPerSecond = 1;
	private bool connected = false;
	private Socket connectionSocket;
	public string STX;
	public string ETX;
	//private NetworkStream stream;
	//private float nextSendTime = 0.0f;
	// Use this for initialization
	void Start () {
		//server.BeginAcceptSocket (connection_made, null);
		System.Net.IPAddress addr;// = new System.Net.IPAddress();
		addr = System.Net.IPAddress.Parse ("127.0.0.1");
		System.Net.IPEndPoint ep = new System.Net.IPEndPoint (addr, 8000);
		server = new TcpListener (ep);
		server.Start();
		Debug.Log ("Waiting for socket to connect");
		connectionSocket = server.AcceptSocket();
		Debug.Log ("Connected!");
		connected = true;
		StartCoroutine (send_frame());


	}
	
	// Update is called once per frame
	void Update () {

	}



		
	IEnumerator send_frame() {
		while (true) {
			
			yield return new WaitForSeconds (1.0f / framesPerSecond);
			yield return new WaitForEndOfFrame ();

			RenderTexture current = RenderTexture.active;

			RenderTexture.active = cam.targetTexture;

			Texture2D image = new Texture2D (cam.targetTexture.width, cam.targetTexture.height, TextureFormat.RGB24, false);


			image.ReadPixels (new Rect (0, 0, cam.targetTexture.width, cam.targetTexture.height), 0, 0);

			byte[] imageData = image.EncodeToJPG (100); //100 % quality

			byte[] telemetry = new byte[sizeof(float) * 4];
			byte[] floatBytes = new byte[4];

			float[] floats = new float[4];
			floats[0] = car.eulerAngles.y;
			floats[1] = car.position.x;
			floats[2] = car.position.y;
			floats[3] = car.position.z;

			for (int i = 0; i < 4; i++) {
				floatBytes = System.BitConverter.GetBytes (floats [i]);
				for (int j = 0; j < 4; j++) {
					telemetry [4 * i + j] = floatBytes [j];
				}
			}
				
			if (connected) {
				connectionSocket.Send (System.Text.Encoding.UTF8.GetBytes(STX));
				connectionSocket.Send (telemetry);
				connectionSocket.Send (imageData);
				connectionSocket.Send (System.Text.Encoding.UTF8.GetBytes(ETX));
			}

			RenderTexture.active = current;
			yield return null;
		}
	}
		
}
