using UnityEngine;

public class ThirdPerson : MonoBehaviour
{
    private const float YMin = 10.0f;
    private const float YMax = 40.0f;
 
    public Transform lookAt;
 
    public Transform Player;
 
    public float distance = 10.0f;
    private float currentX = 0.0f;
    private float currentY = 1.0f;
    public float sensivity = 4.0f;

    public float smoothSpeed = 10f;

    void Start () {
        Cursor.visible = false;
    }
    void LateUpdate ()
    {
        currentX += Input.GetAxis("Mouse X") * sensivity * Time.deltaTime;
        currentY += Input.GetAxis("Mouse Y") * sensivity * Time.deltaTime;
 
        currentY = Mathf.Clamp(currentY, YMin, YMax);
        Vector3 pos = lookAt.position;
        if (lookAt.position.y > 0) {
            pos.y = 2;
        } else {
            pos.y = lookAt.position.y;
        };
        
 
        Vector3 Direction = new Vector3(0, 0, -distance);
        Quaternion rotation = Quaternion.Euler(currentY, currentX, 0);
        Vector3 desiredPosition = lookAt.position + rotation * Direction;
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed * Time.deltaTime);
        transform.position = smoothedPosition;
 
        transform.LookAt(pos);
    }
}
