
using UnityEngine;

public class FollowPlayer : MonoBehaviour
{
    public Transform target;

    public float smoothSpeed = 10f;

    public Vector3 offset;


    void LateUpdate ()
    {
        Vector3 desiredPosition = target.position + offset;
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed * Time.deltaTime);
        transform.position = smoothedPosition;
    }
}
