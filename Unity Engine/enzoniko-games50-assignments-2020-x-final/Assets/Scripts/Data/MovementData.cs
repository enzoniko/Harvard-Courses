using UnityEngine;
using Unity.Entities;

[GenerateAuthoringComponent]
public struct MovementData : IComponentData
{
    public float movementSpeed;
    public float rotationSpeed;
    public KeyCode forwardKey;
    public KeyCode backKey;
    public KeyCode leftKey;
    public KeyCode rightKey;
}