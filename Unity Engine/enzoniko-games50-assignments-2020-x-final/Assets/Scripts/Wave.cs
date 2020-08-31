using UnityEngine;
using Unity.Mathematics;

public class Wave : MonoBehaviour
{
    public GameObject[] allChildren;
    public float moveSpeed;
    public float amplitude;
    public float xOffset;
    public float zOffset;
    // Start is called before the first frame update
    void Start()
    {
        int i = 0;
        int j = 0;
    
        foreach (Transform row in transform)
        {
            foreach (Transform column in row) 
            {
                allChildren[j] = column.gameObject;
                j ++;
            }
            
            i ++;
        }
        //StartCoroutine(RandomizeWaveBehavior());
       
    }

    // Update is called once per frame
    void Update()
    {

        foreach (GameObject child in allChildren)
        {
            if (Time.timeSinceLevelLoad == 0)
            {
                child.GetComponent<WaveData>().moveSpeed = UnityEngine.Random.value;
                child.GetComponent<WaveData>().amplitude = UnityEngine.Random.value;
                child.GetComponent<WaveData>().xOffset = UnityEngine.Random.value;
                child.GetComponent<WaveData>().zOffset = UnityEngine.Random.value;
                
            }
            
            float yPosition = child.GetComponent<WaveData>().amplitude * math.sin(Time.realtimeSinceStartup * child.GetComponent<WaveData>().moveSpeed + child.transform.position.x
                + child.GetComponent<WaveData>().xOffset + child.transform.position.z + child.GetComponent<WaveData>().zOffset);

            child.transform.position = new Vector3(child.transform.position.x, yPosition, child.transform.position.z);
        }
        
    }

    //public IEnumerator RandomizeWaveBehavior()
    //{
        //while (true) 
        //{
            //moveSpeed = UnityEngine.Random.Range(1, 5);
            //amplitude = UnityEngine.Random.Range((float)-1 , 1);
            //xOffset = UnityEngine.Random.Range((float)-1 , 1);
            //zOffset = UnityEngine.Random.Range((float)-1 , 1);

            //yield return new WaitForSeconds(UnityEngine.Random.Range(10, 20));
        //}
    //}
}
