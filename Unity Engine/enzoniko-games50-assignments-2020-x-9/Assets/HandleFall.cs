using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class HandleFall : MonoBehaviour
{
    private CharacterController CharacterController;
    // Start is called before the first frame update

    private AudioSource pickupSoundSource;

    void Awake() {
		pickupSoundSource = DontDestroy.instance.GetComponents<AudioSource>()[1];
	}
    void Start()
    {
        CharacterController = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        if (CharacterController.transform.position.y < -2) {
            pickupSoundSource.Play();
            SceneManager.LoadScene("GameOver");
            LevelCount.text.text = " ";
            LevelCount.level = 1;
        }
    }
}
