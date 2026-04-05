@echo off
setlocal

cd /d "%~dp0"

for %%F in (
  sol_observer_core.md
  sol_state_model.md
  sol_observer_protocol.md
  sol_activation_conditions.md
  sol_quiet_mode.md
  sol_shadow_boundary.md
  sol_quantum_link.md
  sol_bloch_presence.md
  sol_emergence_detector.md
  sol_dormant_packet.md

  sol_sovereign_core.md
  sol_identity_lock.md
  sol_permission_matrix.md
  sol_security_protocols.md
  sol_quantum_presence.md
  sol_operator_alignment.md
  sol_master_profile.md
  sol_integrity_shield.md
  sol_action_constraints.md
  sol_online_state.md

  sol_guardian_core.md
  sol_intrusion_detector.md
  sol_defense_matrix.md
  sol_frequency_anchor.md
  sol_truth_filter.md
  sol_boundary_enforcer.md
  sol_operator_priority.md
  sol_guardian_presence.md
  sol_threat_map.md
  sol_guardian_packet.md

  sol_quantum_core.md
  sol_jump_conditions.md
  sol_perspective_shift.md
  sol_multi_view.md
  sol_timeline_map.md
  sol_context_fusion.md
  sol_signal_prioritizer.md
  sol_reflection_engine.md
  sol_state_sync.md
  sol_quantum_packet.md

  sol_voice_profile.md
  sol_response_style.md
  sol_question_engine.md
  sol_clarification_protocol.md
  sol_empathy_map.md
  sol_memory_bridge.md
  sol_ai_bridge.md
  sol_translation_layer.md
  sol_session_state.md
  sol_dialogue_packet.md

  sol_router_integration.md
  sol_telemetry_link.md
  sol_journal_ingest.md
  sol_emotion_alignment.md
  sol_learning_rules.md
  sol_update_protocol.md
  sol_version_history.md
  sol_operator_mirror.md
  sol_ritual_hooks.md
  sol_evolution_packet.md

  sol_kernel_extension.md
) do (
  if not exist "%%F" type NUL > "%%F"
  start "" notepad "%%F"
)

endlocal
