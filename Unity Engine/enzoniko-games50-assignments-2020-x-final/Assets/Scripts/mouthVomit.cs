using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class mouthVomit : MonoBehaviour
{
    public GameObject vomitCube;
    public GameObject cube;
    public void vomit()
    {
        FindObjectOfType<AudioManager>().Play("VomitSound");
        cube = Instantiate(vomitCube, transform.position, Quaternion.identity);      
    }
}
