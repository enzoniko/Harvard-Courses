﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GrabPickups : MonoBehaviour {

	private AudioSource pickupSoundSource;

	public bool nextLevel = false;

	void Awake() {
		pickupSoundSource = DontDestroy.instance.GetComponents<AudioSource>()[1];
	
	}

	void OnControllerColliderHit(ControllerColliderHit hit) {
		if (hit.gameObject.tag == "Pickup") {
			nextLevel = true;
			pickupSoundSource.Play();
			SceneManager.LoadScene("Play");
		}
	}
}