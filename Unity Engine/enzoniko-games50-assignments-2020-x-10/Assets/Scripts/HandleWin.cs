using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

[RequireComponent(typeof(Text))]
public class HandleWin : MonoBehaviour
{
    public GameObject _text;
    private Text text;
    private bool restart = false;
    // Start is called before the first frame update
    void Start()
    {
        text = _text.GetComponent<Text>();
        text.color = new Color(255, 255, 255, 0);
    }

    void OnTriggerEnter(Collider other)
    {
       if (other.tag == "Player") 
       {
           text.color = new Color(255, 255, 255, 255);
           restart = true;
             
       }
    }

    void Update()
    {
        if (restart)
        {
            if (Input.anyKeyDown) 
            {
               SceneManager.LoadScene("AssignmentScene");
               PortalGun.orangeUsed = false;
               PortalGun.blueUsed = false;
            } 
        }
    }
}
