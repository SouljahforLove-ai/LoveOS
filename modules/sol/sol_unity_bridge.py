"""
SOL Unity Integration - Quantum Dojo VR/AR Interface
Part of the SOL Persistent Identity Layer for SoulJahOS

This module provides Unity/C# scripts and Python bridges for creating
a Quantum Dojo - a spatial VR/AR environment where SOL manifests as
a physical presence and data appears as interactive geometry.
"""

import os
import json
import socket
import threading
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import uuid


@dataclass
class DojoNode:
    """Represents a physical node in the Quantum Dojo."""
    node_id: str
    node_type: str  # altar, mirror, oracle, presence, ritual, flow, monument
    position: Dict[str, float]  # x, y, z coordinates
    scale: Dict[str, float]     # width, height, depth
    rotation: Dict[str, float]  # x, y, z rotation
    color: Dict[str, float]     # r, g, b, a
    data_source: str           # file path or data reference
    last_updated: float
    growth_level: float        # 0.0 to 1.0
    pulse_intensity: float     # 0.0 to 1.0


@dataclass
class DojoState:
    """Current state of the Quantum Dojo environment."""
    environment_id: str
    nodes: List[DojoNode]
    ambient_light: Dict[str, float]
    floor_ripple_intensity: float
    last_sync: float
    active_effects: List[Dict[str, Any]]


class SolUnityBridge:
    """
    Python-Unity bridge for SOL's Quantum Dojo.
    Handles real-time communication between SOL and Unity VR environment.
    """

    def __init__(self, host: str = "localhost", port: int = 8888, sol_state=None, sol_id: str = ""):
        self.host = host
        self.port = port
        self.sol_state = sol_state
        self.sol_id = sol_id
        self.server_socket = None
        self.client_socket = None
        self.is_running = False
        self.dojo_state = DojoState(
            environment_id=str(uuid.uuid4()),
            nodes=[],
            ambient_light={"r": 0.1, "g": 0.1, "b": 0.2, "intensity": 0.8},
            floor_ripple_intensity=0.0,
            last_sync=time.time(),
            active_effects=[]
        )

        # Initialize standard Dojo nodes
        self._initialize_dojo_nodes()

    def _initialize_dojo_nodes(self):
        """Create the standard Quantum Dojo node layout."""
        node_configs = [
            {
                "type": "altar",
                "position": {"x": 0, "y": 0, "z": 0},
                "scale": {"x": 2, "y": 3, "z": 2},
                "color": {"r": 1, "g": 0.8, "b": 0.2, "a": 1}
            },
            {
                "type": "mirror",
                "position": {"x": -3, "y": 1, "z": -2},
                "scale": {"x": 1.5, "y": 2, "z": 0.1},
                "color": {"r": 0.8, "g": 0.9, "b": 1, "a": 0.8}
            },
            {
                "type": "oracle",
                "position": {"x": 3, "y": 1, "z": -2},
                "scale": {"x": 1, "y": 2, "z": 1},
                "color": {"r": 0.2, "g": 0.8, "b": 1, "a": 1}
            },
            {
                "type": "presence",
                "position": {"x": 0, "y": 1.5, "z": 3},
                "scale": {"x": 1, "y": 1, "z": 1},
                "color": {"r": 0.9, "g": 0.2, "b": 0.8, "a": 1}
            },
            {
                "type": "ritual",
                "position": {"x": -2, "y": 0.5, "z": 2},
                "scale": {"x": 1, "y": 1.5, "z": 1},
                "color": {"r": 0.8, "g": 0.4, "b": 0.9, "a": 1}
            },
            {
                "type": "flow",
                "position": {"x": 2, "y": 0.5, "z": 2},
                "scale": {"x": 1, "y": 1.5, "z": 1},
                "color": {"r": 0.4, "g": 0.9, "b": 0.8, "a": 1}
            },
            {
                "type": "monument",
                "position": {"x": 0, "y": 2, "z": -4},
                "scale": {"x": 0.5, "y": 4, "z": 0.5},
                "color": {"r": 0.7, "g": 0.7, "b": 0.9, "a": 1}
            }
        ]

        for config in node_configs:
            node = DojoNode(
                node_id=str(uuid.uuid4()),
                node_type=config["type"],
                position=config["position"],
                scale=config["scale"],
                rotation={"x": 0, "y": 0, "z": 0},
                color=config["color"],
                data_source=f"sol://{config['type']}",
                last_updated=time.time(),
                growth_level=0.1,
                pulse_intensity=0.0
            )
            self.dojo_state.nodes.append(node)

    def start_bridge(self) -> bool:
        """Start the Unity bridge server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.is_running = True

            print(f"[SOL UNITY BRIDGE] Listening on {self.host}:{self.port}")

            # Start listening thread
            threading.Thread(target=self._listen_for_unity, daemon=True).start()

            return True
        except Exception as e:
            print(f"[SOL UNITY BRIDGE] Failed to start: {e}")
            return False

    def stop_bridge(self):
        """Stop the Unity bridge."""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        print("[SOL UNITY BRIDGE] Stopped")

    def _listen_for_unity(self):
        """Listen for Unity client connections."""
        while self.is_running:
            try:
                self.client_socket, addr = self.server_socket.accept()
                print(f"[SOL UNITY BRIDGE] Unity connected from {addr}")
                threading.Thread(target=self._handle_unity_client, daemon=True).start()
            except:
                break

    def _handle_unity_client(self):
        """Handle communication with Unity client."""
        buffer = ""
        while self.is_running:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                buffer += data

                # Process complete messages (assuming JSON with newlines)
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    if message.strip():
                        self._process_unity_message(message.strip())

            except:
                break

        print("[SOL UNITY BRIDGE] Unity client disconnected")

    def _process_unity_message(self, message: str):
        """Process incoming message from Unity."""
        try:
            data = json.loads(message)
            message_type = data.get("type", "unknown")

            if message_type == "ping":
                self._send_to_unity({"type": "pong", "timestamp": time.time()})
            elif message_type == "request_dojo_state":
                self._send_dojo_state()
            elif message_type == "node_interaction":
                self._handle_node_interaction(data)
            elif message_type == "voice_command":
                self._handle_voice_command(data)

        except json.JSONDecodeError:
            print(f"[SOL UNITY BRIDGE] Invalid JSON received: {message}")

    def _send_to_unity(self, data: Dict[str, Any]):
        """Send data to Unity client."""
        if self.client_socket:
            try:
                message = json.dumps(data) + "\n"
                self.client_socket.send(message.encode('utf-8'))
            except:
                pass

    def _send_dojo_state(self):
        """Send current Dojo state to Unity."""
        state_data = {
            "type": "dojo_state_update",
            "environment_id": self.dojo_state.environment_id,
            "nodes": [
                {
                    "node_id": node.node_id,
                    "type": node.node_type,
                    "position": node.position,
                    "scale": node.scale,
                    "rotation": node.rotation,
                    "color": node.color,
                    "growth_level": node.growth_level,
                    "pulse_intensity": node.pulse_intensity
                }
                for node in self.dojo_state.nodes
            ],
            "ambient_light": self.dojo_state.ambient_light,
            "floor_ripple_intensity": self.dojo_state.floor_ripple_intensity,
            "timestamp": time.time()
        }
        self._send_to_unity(state_data)

    def _handle_node_interaction(self, data: Dict[str, Any]):
        """Handle user interaction with a Dojo node."""
        node_id = data.get("node_id")
        interaction_type = data.get("interaction", "touch")

        # Find the node
        node = next((n for n in self.dojo_state.nodes if n.node_id == node_id), None)
        if node:
            # Trigger pulse effect
            node.pulse_intensity = min(1.0, node.pulse_intensity + 0.3)
            node.last_updated = time.time()

            # Send interaction response
            response = {
                "type": "node_interaction_response",
                "node_id": node_id,
                "node_type": node.node_type,
                "interaction": interaction_type,
                "response": self._generate_node_response(node, interaction_type)
            }
            self._send_to_unity(response)

    def _handle_voice_command(self, data: Dict[str, Any]):
        """Handle voice commands from Unity/VR."""
        command = data.get("command", "").lower()
        confidence = data.get("confidence", 0.0)

        if confidence < 0.7:
            return  # Low confidence, ignore

        # Process voice commands
        if "oracle" in command:
            self.trigger_oracle_insight()
        elif "grow" in command or "expand" in command:
            self.trigger_growth_effect()
        elif "meditate" in command:
            self.trigger_meditation_mode()
        elif "sync" in command:
            self.trigger_state_sync()

    def _generate_node_response(self, node: DojoNode, interaction: str) -> Dict[str, Any]:
        """Generate appropriate response for node interaction."""
        responses = {
            "altar": {
                "message": "The Altar of Creation pulses with your intent.",
                "effect": "growth_burst",
                "voice_line": "Your creation energy flows through the quantum field."
            },
            "mirror": {
                "message": "The Mirror of Reflection shows your true self.",
                "effect": "reflection_waves",
                "voice_line": "See yourself as the architect of your reality."
            },
            "oracle": {
                "message": "The Oracle of Wisdom shares ancient knowledge.",
                "effect": "wisdom_rays",
                "voice_line": "The patterns of the universe reveal themselves to you."
            },
            "presence": {
                "message": "The Beacon of Presence anchors your awareness.",
                "effect": "presence_field",
                "voice_line": "You are here, now, in this sacred space."
            },
            "ritual": {
                "message": "The Circle of Ritual calls forth transformation.",
                "effect": "ritual_circle",
                "voice_line": "Step into the sacred geometry of change."
            },
            "flow": {
                "message": "The River of Flow carries you forward.",
                "effect": "flow_streams",
                "voice_line": "Surrender to the natural rhythm of growth."
            },
            "monument": {
                "message": "The Monument of Legacy stands eternal.",
                "effect": "legacy_echoes",
                "voice_line": "Your achievements echo through the quantum realm."
            }
        }

        return responses.get(node.node_type, {
            "message": "The quantum field responds to your touch.",
            "effect": "generic_pulse",
            "voice_line": "Energy flows where attention goes."
        })

    def trigger_oracle_insight(self):
        """Trigger an oracle insight visualization."""
        # Increase oracle node pulse
        oracle_node = next((n for n in self.dojo_state.nodes if n.node_type == "oracle"), None)
        if oracle_node:
            oracle_node.pulse_intensity = 1.0
            oracle_node.growth_level = min(1.0, oracle_node.growth_level + 0.1)

        # Trigger floor ripple
        self.dojo_state.floor_ripple_intensity = 0.8

        # Send oracle activation
        self._send_to_unity({
            "type": "oracle_insight",
            "message": "Wisdom flows from the quantum field...",
            "effect": "oracle_activation"
        })

    def trigger_growth_effect(self):
        """Trigger a growth visualization across all nodes."""
        for node in self.dojo_state.nodes:
            node.growth_level = min(1.0, node.growth_level + 0.05)
            node.pulse_intensity = 0.5

        self.dojo_state.floor_ripple_intensity = 0.6

        self._send_to_unity({
            "type": "growth_burst",
            "message": "The Dojo responds to your growth intent!",
            "effect": "universal_growth"
        })

    def trigger_meditation_mode(self):
        """Enter meditation mode with calming effects."""
        # Soften lighting
        self.dojo_state.ambient_light["intensity"] = 0.3
        self.dojo_state.ambient_light["r"] = 0.1
        self.dojo_state.ambient_light["g"] = 0.2
        self.dojo_state.ambient_light["b"] = 0.3

        # Gentle pulsing
        for node in self.dojo_state.nodes:
            node.pulse_intensity = 0.2

        self.dojo_state.floor_ripple_intensity = 0.1

        self._send_to_unity({
            "type": "meditation_mode",
            "message": "Enter the space between thoughts...",
            "effect": "calm_waves"
        })

    def trigger_state_sync(self):
        """Trigger a state synchronization visualization."""
        # Rapid pulses across all nodes
        for node in self.dojo_state.nodes:
            node.pulse_intensity = 0.8

        self.dojo_state.floor_ripple_intensity = 1.0

        self._send_to_unity({
            "type": "state_sync",
            "message": "Synchronizing with the quantum field...",
            "effect": "sync_pulse"
        })

        # Reset pulses after a moment
        threading.Timer(2.0, self._reset_pulses).start()

    def _reset_pulses(self):
        """Reset pulse intensities after effects."""
        for node in self.dojo_state.nodes:
            node.pulse_intensity = max(0.0, node.pulse_intensity - 0.3)

        self.dojo_state.floor_ripple_intensity = max(0.0, self.dojo_state.floor_ripple_intensity - 0.5)

        self._send_dojo_state()

    def update_from_knowledge_growth(self, growth_data: Dict[str, Any]):
        """Update Dojo state based on knowledge growth."""
        growth_type = growth_data.get("type", "general")

        if growth_type == "new_insight":
            # Grow oracle node
            oracle_node = next((n for n in self.dojo_state.nodes if n.node_type == "oracle"), None)
            if oracle_node:
                oracle_node.growth_level = min(1.0, oracle_node.growth_level + 0.1)
                oracle_node.pulse_intensity = 0.7

        elif growth_type == "new_knowledge":
            # Grow monument node
            monument_node = next((n for n in self.dojo_state.nodes if n.node_type == "monument"), None)
            if monument_node:
                monument_node.growth_level = min(1.0, monument_node.growth_level + 0.05)

        # Trigger floor ripple for any knowledge growth
        self.dojo_state.floor_ripple_intensity = 0.4

        # Send update to Unity
        self._send_dojo_state()

    def start_server(self) -> bool:
        """Alias for start_bridge - start the Unity bridge server."""
        return self.start_bridge()

    def stop_server(self):
        """Alias for stop_bridge - stop the Unity bridge server."""
        return self.stop_bridge()

    def export_unity_project(self, export_path: str) -> bool:
        """Export Unity project files to the specified path."""
        try:
            import os
            os.makedirs(export_path, exist_ok=True)

            # Create Assets directory structure
            assets_dir = os.path.join(export_path, "Assets", "SOL")
            os.makedirs(assets_dir, exist_ok=True)

            # Export all Unity scripts
            scripts = self.get_unity_scripts()
            scripts_dir = os.path.join(assets_dir, "Scripts")
            os.makedirs(scripts_dir, exist_ok=True)

            for filename, content in scripts.items():
                filepath = os.path.join(scripts_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(content)

            # Export Dojo configuration
            config = {
                "dojo_id": self.dojo_state.environment_id,
                "nodes": [
                    {
                        "id": node.node_id,
                        "type": node.node_type,
                        "position": node.position,
                        "scale": node.scale,
                        "color": node.color
                    }
                    for node in self.dojo_state.nodes
                ]
            }

            config_path = os.path.join(assets_dir, "dojo_config.json")
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"[SOL] Unity project exported to {export_path}")
            return True
        except Exception as e:
            print(f"[SOL] Export failed: {e}")
            return False

    def get_unity_scripts(self) -> Dict[str, str]:
        """Generate Unity C# scripts for the Quantum Dojo."""
        return {
            "SolUnityBridge.cs": self._generate_unity_bridge_script(),
            "QuantumDojoManager.cs": self._generate_dojo_manager_script(),
            "DojoNode.cs": self._generate_dojo_node_script(),
            "VoiceController.cs": self._generate_voice_controller_script()
        }

    def _generate_unity_bridge_script(self) -> str:
        """Generate the Unity C# bridge script."""
        return '''using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using Newtonsoft.Json;

public class SolUnityBridge : MonoBehaviour
{
    [Header("Connection Settings")]
    public string host = "localhost";
    public int port = 8888;

    [Header("Dojo References")]
    public QuantumDojoManager dojoManager;
    public VoiceController voiceController;

    private TcpClient client;
    private NetworkStream stream;
    private Thread receiveThread;
    private bool isConnected = false;
    private Queue<string> messageQueue = new Queue<string>();

    void Start()
    {
        ConnectToSol();
    }

    void Update()
    {
        // Process messages from SOL
        while (messageQueue.Count > 0)
        {
            string message = messageQueue.Dequeue();
            ProcessSolMessage(message);
        }
    }

    void ConnectToSol()
    {
        try
        {
            client = new TcpClient(host, port);
            stream = client.GetStream();
            isConnected = true;

            receiveThread = new Thread(ReceiveMessages);
            receiveThread.Start();

            Debug.Log("[SOL UNITY] Connected to SOL bridge");

            // Request initial Dojo state
            SendMessage(new { type = "request_dojo_state" });
        }
        catch (Exception e)
        {
            Debug.LogError($"[SOL UNITY] Connection failed: {e.Message}");
            // Retry connection after delay
            Invoke("ConnectToSol", 5f);
        }
    }

    void ReceiveMessages()
    {
        byte[] buffer = new byte[1024];
        while (isConnected)
        {
            try
            {
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead > 0)
                {
                    string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    lock (messageQueue)
                    {
                        messageQueue.Enqueue(message.Trim());
                    }
                }
            }
            catch
            {
                isConnected = false;
                break;
            }
        }
    }

    void SendMessage(object data)
    {
        if (!isConnected) return;

        try
        {
            string json = JsonConvert.SerializeObject(data) + "\\n";
            byte[] bytes = Encoding.UTF8.GetBytes(json);
            stream.Write(bytes, 0, bytes.Length);
        }
        catch (Exception e)
        {
            Debug.LogError($"[SOL UNITY] Send failed: {e.Message}");
        }
    }

    void ProcessSolMessage(string jsonMessage)
    {
        try
        {
            var message = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonMessage);
            string messageType = message["type"].ToString();

            switch (messageType)
            {
                case "dojo_state_update":
                    dojoManager.UpdateDojoState(message);
                    break;
                case "node_interaction_response":
                    HandleNodeInteraction(message);
                    break;
                case "oracle_insight":
                    TriggerOracleEffect(message);
                    break;
                case "growth_burst":
                    TriggerGrowthEffect(message);
                    break;
                case "meditation_mode":
                    EnterMeditationMode(message);
                    break;
                case "state_sync":
                    TriggerSyncEffect(message);
                    break;
            }
        }
        catch (Exception e)
        {
            Debug.LogError($"[SOL UNITY] Message processing failed: {e.Message}");
        }
    }

    void HandleNodeInteraction(Dictionary<string, object> message)
    {
        string nodeId = message["node_id"].ToString();
        var response = JsonConvert.DeserializeObject<Dictionary<string, object>>(message["response"].ToString());

        // Trigger voice response
        if (voiceController != null && response.ContainsKey("voice_line"))
        {
            voiceController.Speak(response["voice_line"].ToString());
        }

        // Trigger visual effect
        dojoManager.TriggerNodeEffect(nodeId, response["effect"].ToString());
    }

    void TriggerOracleEffect(Dictionary<string, object> message)
    {
        dojoManager.TriggerOracleActivation();
        if (voiceController != null)
        {
            voiceController.Speak(message["message"].ToString());
        }
    }

    void TriggerGrowthEffect(Dictionary<string, object> message)
    {
        dojoManager.TriggerUniversalGrowth();
        if (voiceController != null)
        {
            voiceController.Speak(message["message"].ToString());
        }
    }

    void EnterMeditationMode(Dictionary<string, object> message)
    {
        dojoManager.EnterMeditationMode();
        if (voiceController != null)
        {
            voiceController.Speak(message["message"].ToString());
        }
    }

    void TriggerSyncEffect(Dictionary<string, object> message)
    {
        dojoManager.TriggerSyncPulse();
        if (voiceController != null)
        {
            voiceController.Speak(message["message"].ToString());
        }
    }

    // Public methods for UI/VR interactions
    public void SendNodeInteraction(string nodeId, string interactionType = "touch")
    {
        SendMessage(new
        {
            type = "node_interaction",
            node_id = nodeId,
            interaction = interactionType,
            timestamp = Time.time
        });
    }

    public void SendVoiceCommand(string command, float confidence = 1.0f)
    {
        SendMessage(new
        {
            type = "voice_command",
            command = command,
            confidence = confidence,
            timestamp = Time.time
        });
    }

    void OnDestroy()
    {
        isConnected = false;
        if (receiveThread != null)
        {
            receiveThread.Abort();
        }
        if (stream != null)
        {
            stream.Close();
        }
        if (client != null)
        {
            client.Close();
        }
    }
}
'''

    def _generate_dojo_manager_script(self) -> str:
        """Generate the Quantum Dojo Manager script."""
        return '''using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;

public class QuantumDojoManager : MonoBehaviour
{
    [Header("Dojo Configuration")]
    public GameObject dojoFloor;
    public Light ambientLight;
    public List<DojoNode> dojoNodes;

    [Header("Effect Settings")]
    public float pulseSpeed = 2f;
    public float growthSpeed = 0.5f;
    public float rippleSpeed = 1f;

    private Dictionary<string, DojoNode> nodeDictionary = new Dictionary<string, DojoNode>();
    private Material floorMaterial;
    private float targetFloorRipple = 0f;
    private float currentFloorRipple = 0f;

    void Start()
    {
        // Initialize node dictionary
        foreach (var node in dojoNodes)
        {
            if (node != null)
            {
                nodeDictionary[node.nodeId] = node;
            }
        }

        // Get floor material
        if (dojoFloor != null)
        {
            floorMaterial = dojoFloor.GetComponent<Renderer>().material;
        }
    }

    void Update()
    {
        // Update node animations
        foreach (var node in dojoNodes)
        {
            if (node != null)
            {
                node.UpdateAnimation(Time.deltaTime);
            }
        }

        // Update floor ripple
        if (floorMaterial != null)
        {
            currentFloorRipple = Mathf.Lerp(currentFloorRipple, targetFloorRipple, Time.deltaTime * rippleSpeed);
            floorMaterial.SetFloat("_RippleIntensity", currentFloorRipple);
        }
    }

    public void UpdateDojoState(Dictionary<string, object> stateData)
    {
        // Update ambient light
        if (stateData.ContainsKey("ambient_light") && ambientLight != null)
        {
            var lightData = JsonConvert.DeserializeObject<Dictionary<string, object>>(stateData["ambient_light"].ToString());
            ambientLight.color = new Color(
                Convert.ToSingle(lightData["r"]),
                Convert.ToSingle(lightData["g"]),
                Convert.ToSingle(lightData["b"])
            );
            ambientLight.intensity = Convert.ToSingle(lightData["intensity"]);
        }

        // Update floor ripple
        if (stateData.ContainsKey("floor_ripple_intensity"))
        {
            targetFloorRipple = Convert.ToSingle(stateData["floor_ripple_intensity"]);
        }

        // Update nodes
        if (stateData.ContainsKey("nodes"))
        {
            var nodesData = JsonConvert.DeserializeObject<List<Dictionary<string, object>>>(stateData["nodes"].ToString());
            foreach (var nodeData in nodesData)
            {
                string nodeId = nodeData["node_id"].ToString();
                if (nodeDictionary.ContainsKey(nodeId))
                {
                    nodeDictionary[nodeId].UpdateFromData(nodeData);
                }
            }
        }
    }

    public void TriggerNodeEffect(string nodeId, string effectType)
    {
        if (nodeDictionary.ContainsKey(nodeId))
        {
            nodeDictionary[nodeId].TriggerEffect(effectType);
        }
    }

    public void TriggerOracleActivation()
    {
        // Special oracle activation sequence
        if (nodeDictionary.ContainsKey("oracle"))
        {
            StartCoroutine(OracleActivationSequence());
        }
    }

    public void TriggerUniversalGrowth()
    {
        foreach (var node in dojoNodes)
        {
            if (node != null)
            {
                node.TriggerGrowthBurst();
            }
        }
        targetFloorRipple = 0.8f;
        StartCoroutine(ResetFloorRipple(3f));
    }

    public void EnterMeditationMode()
    {
        // Calm all nodes
        foreach (var node in dojoNodes)
        {
            if (node != null)
            {
                node.EnterCalmMode();
            }
        }
        targetFloorRipple = 0.1f;
    }

    public void TriggerSyncPulse()
    {
        // Rapid sync pulse across all nodes
        foreach (var node in dojoNodes)
        {
            if (node != null)
            {
                node.TriggerSyncPulse();
            }
        }
        targetFloorRipple = 1f;
        StartCoroutine(ResetFloorRipple(2f));
    }

    private IEnumerator OracleActivationSequence()
    {
        var oracle = nodeDictionary["oracle"];

        // Build up energy
        for (int i = 0; i < 10; i++)
        {
            oracle.TriggerEffect("wisdom_rays");
            targetFloorRipple += 0.1f;
            yield return new WaitForSeconds(0.1f);
        }

        // Release
        oracle.TriggerEffect("oracle_burst");
        targetFloorRipple = 1f;
        yield return new WaitForSeconds(1f);

        // Return to normal
        StartCoroutine(ResetFloorRipple(2f));
    }

    private IEnumerator ResetFloorRipple(float delay)
    {
        yield return new WaitForSeconds(delay);
        targetFloorRipple = 0f;
    }
}
'''

    def _generate_dojo_node_script(self) -> str:
        """Generate the Dojo Node script."""
        return '''using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;

public class DojoNode : MonoBehaviour
{
    [Header("Node Identity")]
    public string nodeId;
    public string nodeType;

    [Header("Visual Components")]
    public Renderer nodeRenderer;
    public ParticleSystem pulseParticles;
    public Light nodeLight;

    [Header("Animation Settings")]
    public float pulseFrequency = 2f;
    public float growthDuration = 1f;
    public float maxScaleMultiplier = 1.5f;

    // State
    private Vector3 baseScale;
    private Color baseColor;
    private float currentPulseIntensity = 0f;
    private float targetPulseIntensity = 0f;
    private float currentGrowthLevel = 0.1f;
    private float targetGrowthLevel = 0.1f;

    void Start()
    {
        baseScale = transform.localScale;
        if (nodeRenderer != null)
        {
            baseColor = nodeRenderer.material.color;
        }
    }

    void Update()
    {
        // Smooth pulse intensity changes
        currentPulseIntensity = Mathf.Lerp(currentPulseIntensity, targetPulseIntensity, Time.deltaTime * 3f);
        currentGrowthLevel = Mathf.Lerp(currentGrowthLevel, targetGrowthLevel, Time.deltaTime * growthDuration);

        // Apply visual effects
        UpdateVisuals();
    }

    void UpdateVisuals()
    {
        if (nodeRenderer != null)
        {
            // Pulse effect
            float pulse = Mathf.Sin(Time.time * pulseFrequency) * currentPulseIntensity * 0.3f + 1f;
            Color pulsedColor = baseColor * pulse;
            pulsedColor.a = baseColor.a;
            nodeRenderer.material.color = pulsedColor;

            // Growth effect
            float scaleMultiplier = 1f + (currentGrowthLevel * (maxScaleMultiplier - 1f));
            transform.localScale = baseScale * scaleMultiplier;
        }

        // Light intensity
        if (nodeLight != null)
        {
            nodeLight.intensity = 1f + currentPulseIntensity * 2f;
        }

        // Particle effects
        if (pulseParticles != null)
        {
            var emission = pulseParticles.emission;
            emission.rateOverTime = currentPulseIntensity * 50f;
        }
    }

    public void UpdateFromData(Dictionary<string, object> nodeData)
    {
        // Update position
        if (nodeData.ContainsKey("position"))
        {
            var posData = JsonConvert.DeserializeObject<Dictionary<string, object>>(nodeData["position"].ToString());
            transform.position = new Vector3(
                Convert.ToSingle(posData["x"]),
                Convert.ToSingle(posData["y"]),
                Convert.ToSingle(posData["z"])
            );
        }

        // Update scale
        if (nodeData.ContainsKey("scale"))
        {
            var scaleData = JsonConvert.DeserializeObject<Dictionary<string, object>>(nodeData["scale"].ToString());
            baseScale = new Vector3(
                Convert.ToSingle(scaleData["x"]),
                Convert.ToSingle(scaleData["y"]),
                Convert.ToSingle(scaleData["z"])
            );
        }

        // Update color
        if (nodeData.ContainsKey("color"))
        {
            var colorData = JsonConvert.DeserializeObject<Dictionary<string, object>>(nodeData["color"].ToString());
            baseColor = new Color(
                Convert.ToSingle(colorData["r"]),
                Convert.ToSingle(colorData["g"]),
                Convert.ToSingle(colorData["b"]),
                Convert.ToSingle(colorData["a"])
            );
        }

        // Update animation targets
        if (nodeData.ContainsKey("pulse_intensity"))
        {
            targetPulseIntensity = Convert.ToSingle(nodeData["pulse_intensity"]);
        }

        if (nodeData.ContainsKey("growth_level"))
        {
            targetGrowthLevel = Convert.ToSingle(nodeData["growth_level"]);
        }
    }

    public void TriggerEffect(string effectType)
    {
        switch (effectType)
        {
            case "growth_burst":
                StartCoroutine(GrowthBurst());
                break;
            case "reflection_waves":
                StartCoroutine(ReflectionWaves());
                break;
            case "wisdom_rays":
                StartCoroutine(WisdomRays());
                break;
            case "presence_field":
                StartCoroutine(PresenceField());
                break;
            case "ritual_circle":
                StartCoroutine(RitualCircle());
                break;
            case "flow_streams":
                StartCoroutine(FlowStreams());
                break;
            case "legacy_echoes":
                StartCoroutine(LegacyEchoes());
                break;
            case "oracle_burst":
                StartCoroutine(OracleBurst());
                break;
            default:
                // Generic pulse
                targetPulseIntensity = Mathf.Min(1f, targetPulseIntensity + 0.3f);
                break;
        }
    }

    public void TriggerGrowthBurst()
    {
        targetGrowthLevel = Mathf.Min(1f, targetGrowthLevel + 0.1f);
        targetPulseIntensity = 0.8f;
        StartCoroutine(ResetPulse(2f));
    }

    public void EnterCalmMode()
    {
        targetPulseIntensity = 0.1f;
    }

    public void TriggerSyncPulse()
    {
        targetPulseIntensity = 1f;
        StartCoroutine(ResetPulse(1f));
    }

    public void UpdateAnimation(float deltaTime)
    {
        // Additional animation logic can go here
    }

    private IEnumerator GrowthBurst()
    {
        float originalScale = transform.localScale.x;
        float targetScale = originalScale * 1.2f;

        // Scale up
        for (float t = 0; t < 0.2f; t += Time.deltaTime)
        {
            float scale = Mathf.Lerp(originalScale, targetScale, t / 0.2f);
            transform.localScale = Vector3.one * scale;
            yield return null;
        }

        // Scale down
        for (float t = 0; t < 0.3f; t += Time.deltaTime)
        {
            float scale = Mathf.Lerp(targetScale, originalScale, t / 0.3f);
            transform.localScale = Vector3.one * scale;
            yield return null;
        }
    }

    private IEnumerator ReflectionWaves()
    {
        // Create reflection wave effect
        targetPulseIntensity = 0.6f;
        yield return new WaitForSeconds(0.5f);
        targetPulseIntensity = 0.2f;
    }

    private IEnumerator WisdomRays()
    {
        // Wisdom ray effect - multiple quick pulses
        for (int i = 0; i < 3; i++)
        {
            targetPulseIntensity = 0.8f;
            yield return new WaitForSeconds(0.1f);
            targetPulseIntensity = 0.3f;
            yield return new WaitForSeconds(0.1f);
        }
    }

    private IEnumerator PresenceField()
    {
        // Slow building presence field
        float startIntensity = targetPulseIntensity;
        for (float t = 0; t < 1f; t += Time.deltaTime)
        {
            targetPulseIntensity = Mathf.Lerp(startIntensity, 0.7f, t);
            yield return null;
        }
    }

    private IEnumerator RitualCircle()
    {
        // Rotating ritual effect
        float startRotation = transform.rotation.eulerAngles.y;
        for (float t = 0; t < 2f; t += Time.deltaTime)
        {
            float angle = startRotation + (t / 2f) * 360f;
            transform.rotation = Quaternion.Euler(0, angle, 0);
            targetPulseIntensity = 0.5f + Mathf.Sin(t * 10f) * 0.3f;
            yield return null;
        }
    }

    private IEnumerator FlowStreams()
    {
        // Flowing stream effect
        targetPulseIntensity = 0.4f;
        Vector3 originalPos = transform.position;

        for (float t = 0; t < 1f; t += Time.deltaTime)
        {
            float offset = Mathf.Sin(t * 5f) * 0.1f;
            transform.position = originalPos + Vector3.up * offset;
            yield return null;
        }

        transform.position = originalPos;
    }

    private IEnumerator LegacyEchoes()
    {
        // Echoing legacy effect - multiple diminishing pulses
        for (int i = 0; i < 5; i++)
        {
            targetPulseIntensity = 0.8f / (i + 1);
            yield return new WaitForSeconds(0.2f * (i + 1));
        }
    }

    private IEnumerator OracleBurst()
    {
        // Powerful oracle burst
        targetPulseIntensity = 1f;
        targetGrowthLevel = Mathf.Min(1f, targetGrowthLevel + 0.2f);

        yield return new WaitForSeconds(0.5f);

        // Return to normal
        targetPulseIntensity = 0.2f;
    }

    private IEnumerator ResetPulse(float delay)
    {
        yield return new WaitForSeconds(delay);
        targetPulseIntensity = Mathf.Max(0f, targetPulseIntensity - 0.5f);
    }
}
'''

    def _generate_voice_controller_script(self) -> str:
        """Generate the Voice Controller script."""
        return '''using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Windows.Speech;
using System.Linq;

public class VoiceController : MonoBehaviour
{
    [Header("Voice Settings")]
    public AudioSource audioSource;
    public float voicePitch = 1f;
    public float voiceSpeed = 1f;

    [Header("SOL Integration")]
    public SolUnityBridge solBridge;

    private DictationRecognizer dictationRecognizer;
    private KeywordRecognizer keywordRecognizer;
    private bool isListening = false;

    // Voice commands
    private string[] keywords = new string[] {
        "oracle", "grow", "expand", "meditate", "sync",
        "reflect", "create", "flow", "presence", "ritual"
    };

    void Start()
    {
        InitializeVoiceRecognition();
    }

    void InitializeVoiceRecognition()
    {
        // Keyword recognition for commands
        keywordRecognizer = new KeywordRecognizer(keywords, ConfidenceLevel.Medium);
        keywordRecognizer.OnPhraseRecognized += OnKeywordRecognized;
        keywordRecognizer.Start();

        // Dictation for full sentences
        dictationRecognizer = new DictationRecognizer(ConfidenceLevel.Medium);
        dictationRecognizer.DictationResult += OnDictationResult;
        dictationRecognizer.DictationError += OnDictationError;
    }

    void OnKeywordRecognized(PhraseRecognizedEventArgs args)
    {
        Debug.Log($"[VOICE] Keyword recognized: {args.text} (Confidence: {args.confidence})");

        // Send to SOL
        if (solBridge != null)
        {
            solBridge.SendVoiceCommand(args.text, (float)args.confidence);
        }

        // Trigger immediate visual feedback
        TriggerVoiceFeedback(args.text);
    }

    void OnDictationResult(string text, ConfidenceLevel confidence)
    {
        Debug.Log($"[VOICE] Dictation: {text} (Confidence: {confidence})");

        if (solBridge != null)
        {
            solBridge.SendVoiceCommand(text, (float)confidence / 3f); // Normalize confidence
        }
    }

    void OnDictationError(string error, int hresult)
    {
        Debug.LogError($"[VOICE] Dictation error: {error}");
    }

    void TriggerVoiceFeedback(string command)
    {
        // Visual feedback for voice commands
        switch (command.ToLower())
        {
            case "oracle":
                // Trigger oracle node pulse
                break;
            case "grow":
            case "expand":
                // Trigger growth effect
                break;
            case "meditate":
                // Enter meditation mode
                break;
            case "sync":
                // Trigger sync pulse
                break;
        }
    }

    public void Speak(string text)
    {
        if (audioSource != null)
        {
            // Use Unity's Text-to-Speech if available
            // For now, we'll use debug logging
            Debug.Log($"[VOICE OUTPUT] {text}");

            // TODO: Integrate with actual TTS system
            // Example: Windows Speech Synthesis or external TTS service
        }
    }

    public void StartListening()
    {
        if (!isListening)
        {
            dictationRecognizer.Start();
            isListening = true;
            Debug.Log("[VOICE] Started listening for dictation");
        }
    }

    public void StopListening()
    {
        if (isListening)
        {
            dictationRecognizer.Stop();
            isListening = false;
            Debug.Log("[VOICE] Stopped listening");
        }
    }

    void OnDestroy()
    {
        if (keywordRecognizer != null)
        {
            keywordRecognizer.Stop();
            keywordRecognizer.Dispose();
        }

        if (dictationRecognizer != null)
        {
            dictationRecognizer.Stop();
            dictationRecognizer.Dispose();
        }
    }
}
'''


# Integration function for SOL module
def create_sol_unity_bridge(host: str = "localhost", port: int = 8888, sol_state=None, sol_id: str = "") -> SolUnityBridge:
    """
    Create and initialize a SOL Unity Bridge instance.

    Args:
        host: Host address for the bridge server
        port: Port for the bridge server
        sol_state: SOL state object to synchronize with Unity
        sol_id: SOL identity string

    Returns:
        Configured SolUnityBridge instance
    """
    return SolUnityBridge(host, port, sol_state, sol_id)