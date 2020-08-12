using System.Collections;
using UnityEngine.UI;
using UnityEngine;

[RequireComponent(typeof(Text))]
public class LevelCount : MonoBehaviour
{
    public GameObject controller;
    public static Text text;

    public static int level = 1;
  
    // Start is called before the first frame update
    void Start()
    {
        text = GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
        if (controller.GetComponent<GrabPickups>().nextLevel) {
            level += 1;
        }
        if (text.text == " " && level == 1) {

        }else {
           text.text = "Level: " + level; 
        }
    }
}
