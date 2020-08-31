using System.Collections;
using UnityEngine;
public class Player : MonoBehaviour
{
    [SerializeField]
    private float _moveSpeed = 5f;
    [SerializeField]
    private float _gravity = 9.81f;
    [SerializeField]
    private float _jumpSpeed = 3.5f;
    public HealthBar healthBar;
    public CharacterController _controller;
    public bool stuck = false;
    public Material red;
    public Material green;
    public Material yellow;
    public Transform Cam;

    public Vector3 SpawnPos = new Vector3(4f, 4f, 4f);
    public GameObject mouth;

    private float _directionY;

    // Start is called before the first frame update
    void Start()
    {
        DataBaseManager.refreshCurrentScene();
        //currentHealth = maxHealth;
        //healthBar.SetMaxHealth(maxHealth);
        _controller = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        //Debug.Log(Database.currentScene);
        Database.currentMaterial = gameObject.GetComponent<MeshRenderer>().material;

        float Horizontal = Input.GetAxis("Horizontal") * _moveSpeed * Time.deltaTime;
        float Vertical = Input.GetAxis("Vertical") * _moveSpeed * Time.deltaTime;

        Vector3 Movement = Cam.transform.right * Horizontal + Cam.transform.forward * Vertical;

        if (Movement.magnitude != 0f)
        {
            transform.Rotate(Vector3.up * Input.GetAxis("Mouse X") * Cam.GetComponent<ThirdPerson>().sensivity * Time.deltaTime);
 
            Quaternion CamRotation = Cam.rotation;
            CamRotation.x = 0f;
            CamRotation.z = 0f;
 
            transform.rotation = Quaternion.Lerp(transform.rotation, CamRotation, 0.1f);
        }

        if (transform.localScale.z > 1f)
        {
            gameObject.GetComponent<MeshRenderer>().material = green;
            gameObject.GetComponentInChildren<Light>().color = Color.green;
        }
        if(transform.localScale.z == 3f) 
        {
            gameObject.GetComponent<MeshRenderer>().material = yellow;
            gameObject.GetComponentInChildren<Light>().color = Color.yellow;
        } 
        if(transform.localScale.z == 1f){
            gameObject.GetComponent<MeshRenderer>().material = red;
            gameObject.GetComponentInChildren<Light>().color = Color.red;
            stuck = false;
        };
        if (Database.currentScene == "1PlayerMode")
        {
            if (Input.GetKeyDown(KeyCode.B) && transform.position.x > 8f && transform.position.z > 8f && transform.position.x < 23f && transform.position.z < 23f && transform.localScale.z > 1f && transform.position.y > -5f && stuck == false)
            {
                stuck = true;
                StartCoroutine("vomit"); 
            }
        }
        if (Database.currentScene == "QuickMode")
        {
            if (Input.GetKeyDown(KeyCode.B) && transform.position.x > 8f && transform.position.z > 8f && transform.position.x < 23f && transform.position.z < 23f && transform.localScale.z > 1f && transform.position.y > -5f)
            {
                stuck = true;
                StartCoroutine("vomit"); 
            }
        }
        
        
        if (_controller.isGrounded)
        {
            _moveSpeed = 15f;

            if (Input.GetButtonDown("Jump") && stuck == false)
            {
                FindObjectOfType<AudioManager>().Play("JumpSound");
                _directionY = _jumpSpeed;
            }
        } else {
            _directionY -= _gravity * Time.deltaTime;
            if(transform.position.y < -500f) 
            {
                _controller.enabled = false;
                transform.position = SpawnPos;
                _controller.enabled = true;
                transform.localScale = new Vector3(1,1,1);
                TakeDamage(1);
            };
        };

        if(transform.position.y < 0f) 
        {
            _directionY -= 0.5f * Time.deltaTime;
        };

        if(stuck)
        {
            _moveSpeed = 0f;
        }

        if(Database.currentHealth == 0)
        {
            DataBaseManager.goToScene("GameOver");
            FindObjectOfType<AudioManager>().Play("GameOver");
        }

        Movement.y = _directionY;

        _controller.Move(Movement);      
    }
    void TakeDamage(int damage)
	{
		Database.currentHealth -= damage;
        FindObjectOfType<AudioManager>().Play("TakeDamage");
		healthBar.SetHealth(Database.currentHealth);
	}
    public void OnCollisionEnter(Collision col) {
        if (col.gameObject.GetComponent<foodScript>() && transform.localScale.z < 3f)
        {
            eat();
            Destroy(col.gameObject);
        }
    }

    public void eat()
    {
        FindObjectOfType<AudioManager>().Play("EatSound");
        DataBaseManager.addScore(10 * Database.currentHealth);
        float ScaleX = Mathf.Clamp(transform.localScale.x + 0.5f, 1f, 3f);
        float ScaleY = Mathf.Clamp(transform.localScale.y + 0.5f, 1f, 3f);
        float ScaleZ = Mathf.Clamp(transform.localScale.z + 0.5f, 1f, 3f);
        transform.localScale = new Vector3(ScaleX, ScaleY, ScaleZ);
        
    }

    public IEnumerator vomit()
    {
        while(transform.localScale.z > 1 && transform.localScale.z <= 3)
        {
            
            float ScaleX = Mathf.Clamp(transform.localScale.x - 0.1f, 1f, 3f);
            float ScaleY = Mathf.Clamp(transform.localScale.y - 0.1f, 1f, 3f);
            float ScaleZ = Mathf.Clamp(transform.localScale.z - 0.1f, 1f, 3f);
            transform.localScale = new Vector3(ScaleX, ScaleY, ScaleZ);
            mouth.GetComponent<mouthVomit>().vomit();
            DataBaseManager.AddSeconds(2f);
            DataBaseManager.addScore(10 * Database.currentHealth);
            yield return new WaitForSecondsRealtime(0.5f);
        }  
    }
}
