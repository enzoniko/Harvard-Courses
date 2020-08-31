using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cubeSpawner : MonoBehaviour
{
    public GameObject cubePrefab;

    public Vector3 position;

    List<GameObject> objects = new List<GameObject>();

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(spawnCubes());
        StartCoroutine(spawnCubes());
        // if (Time.realtimeSinceStartup > 60)
        // {
        //     StartCoroutine(spawnCubes());
        // }
        // if (Time.realtimeSinceStartup > 180)
        // {
        //     StartCoroutine(spawnCubes());
        //     StartCoroutine(spawnCubes());
        // }
        StartCoroutine(destroyCubes());
    }

    public IEnumerator spawnCubes() {
        while(true) 
        {
            position = new Vector3(Random.Range(0, 31), 15, Random.Range(0, 31));
            objects.Add(Instantiate(
                cubePrefab,
                position,
                Quaternion.identity
            ));
            yield return new WaitForSecondsRealtime(Random.Range(3, 7));
            
        }
        
    }

    public IEnumerator destroyCubes() {
        while(true) 
        {
            Destroy(objects[0]);
            objects.Remove(objects[0]);
            yield return new WaitForSecondsRealtime(10);
        }
        
    }
}
