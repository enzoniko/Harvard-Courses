using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[RequireComponent(typeof(SphereCollider))]

public class blackHole : MonoBehaviour {
    [SerializeField] public float GRAVITY_PULL = .78f;
    public float m_GravityRadius = 1f;
    public GameObject sphere;
    public List<Collider> blackHoleCubes = new List<Collider>();
    void Awake()
    {
        m_GravityRadius = GetComponent<SphereCollider>().radius;
    }
    /// <summary>
    /// Attract objects towards an area when they come within the bounds of a collider.
    /// This function is on the physics timer so it won't necessarily run every frame.
    /// </summary>
    /// <param name="other">Any object within reach of gravity's collider</param>
    void OnTriggerStay(Collider other)
    {
        if(other.attachedRigidbody && other.GetComponent<VomitScript>())
        {
            float gravityIntensity = Vector3.Distance(transform.position, other.transform.position) / m_GravityRadius;
            other.attachedRigidbody.AddForce((transform.position - other.transform.position) * gravityIntensity * other.attachedRigidbody.mass * GRAVITY_PULL * Time.smoothDeltaTime);
            Debug.DrawRay(other.transform.position, transform.position - other.transform.position);
            if (blackHoleCubes.Contains(other) && other.transform.position.x > 15f && other.transform.position.z > 15f && other.transform.position.x < 16f && other.transform.position.z < 16f)
            {
                blackHoleCubes.Remove(other);
                Destroy(other.gameObject);
            }   
            if (!blackHoleCubes.Contains(other) && sphere.transform.localScale.z > 10)
            {
                Destroy(other.gameObject);
            }
        }
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.GetComponentInParent<ThirdPerson>() && sphere.transform.localScale.z > 10)
        {
            if (Database.currentScene == "1PlayerMode")
            {
                Database.maxTime += 2f;
                DataBaseManager.AddSeconds(Time.realtimeSinceStartup/Database.blackHoleCubesNumber * Database.currentHealth);
                //foodValue = foodValue - (foodValue/100 * 10);
                DataBaseManager.goToScene("1PlayerMode");
                DataBaseManager.newRound();
                DataBaseManager.addScore((int)Time.realtimeSinceStartup/Database.blackHoleCubesNumber * Database.currentHealth * (int)Database.timeLeft);
            }
            if (Database.currentScene == "QuickMode")
            {
                FindObjectOfType<AudioManager>().Play("NextRound");
                Database.maxTime -= 2f;
                DataBaseManager.AddSeconds(Time.realtimeSinceStartup/Database.blackHoleCubesNumber * Database.currentHealth);
                DataBaseManager.reduceFoodValueBy(0.1f);
                DataBaseManager.handleRoundChanging();
                DataBaseManager.addScore((int)Time.realtimeSinceStartup/Database.blackHoleCubesNumber * Database.currentHealth * (int)Database.timeLeft);
            }
        }

        if(other.attachedRigidbody && other.GetComponent<VomitScript>()) 
        {
            if (!blackHoleCubes.Contains(other) && sphere.transform.localScale.z <= 10)
            {
                eat();
                blackHoleCubes.Add(other);
                DataBaseManager.increaseBlackHoleCubesNumber();
            }
        }  
    }
 
    public void eat()
    {
        if (Database.currentScene == "1PlayerMode")
        {
            float ScaleX = Mathf.Clamp(sphere.transform.localScale.x + Database.foodValue, 1f, 10f);
            float ScaleY = Mathf.Clamp(sphere.transform.localScale.y + Database.foodValue, 1f, 10f);
            float ScaleZ = Mathf.Clamp(sphere.transform.localScale.z + Database.foodValue, 1f, 10f);
            sphere.transform.localScale = new Vector3(ScaleX, ScaleY, ScaleZ);
            if (sphere.transform.localScale.z == 10)
            {
                StartCoroutine("grow");
            }
        }
        if (Database.currentScene == "QuickMode")
        {
            float ScaleX = Mathf.Clamp(sphere.transform.localScale.x + Database.foodValue, 1f, 10f);
            float ScaleY = Mathf.Clamp(sphere.transform.localScale.y + Database.foodValue, 1f, 10f);
            float ScaleZ = Mathf.Clamp(sphere.transform.localScale.z + Database.foodValue, 1f, 10f);
            sphere.transform.localScale = new Vector3(ScaleX, ScaleY, ScaleZ);
            if (sphere.transform.localScale.z == 10)
            {
                StartCoroutine("grow");
            }
        }
        
    }

    public IEnumerator destroyCubes() 
    {
        while(blackHoleCubes[0]) 
        {
            Destroy(blackHoleCubes[0]);
            blackHoleCubes.Remove(blackHoleCubes[0]);
            yield return new WaitForSecondsRealtime(5);
        }
    }

    public IEnumerator grow()
    {
        while (transform.localScale.z < 51)
        {
            float ScaleX = Mathf.Clamp(sphere.transform.localScale.x + 10f * Time.deltaTime, 1f, 50f);
            float ScaleY = Mathf.Clamp(sphere.transform.localScale.y + 10f * Time.deltaTime, 1f, 50f);
            float ScaleZ = Mathf.Clamp(sphere.transform.localScale.z + 10f * Time.deltaTime, 1f, 50f);
            sphere.transform.localScale = new Vector3(ScaleX, ScaleY, ScaleZ);
            gameObject.GetComponent<SphereCollider>().radius = sphere.transform.localScale.x/2 + 2f;
            yield return null;
        }
    }
}