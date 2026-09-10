# SME Review Sheet

**Publish version:** `publish_20260720_113410_7e830fa4`  
**Generated:** 2026-07-20T11:34:29.139313+00:00

## Corpus counts

- **runbooks:** 401
- **playbooks_prompt_a:** 4
- **playbooks_prompt_b:** 7
- **embeddings_total:** 1261
- **embeddings_runbooks:** 401
- **embeddings_playbooks_prompt_a:** 4
- **embeddings_playbooks_prompt_b:** 7
- **embeddings_operational_context:** 590
- **embeddings_source_artifacts:** 259
- **operational_context_rag:** 590
- **source_artifacts_rag:** 259
- **canonical_images:** 251
- **canonical_images_with_storage_uri:** 251
- **relationship_links:** 17619
- **relationship_shards:** 9

## Cosmos containers

- **runbooks:** `runbooks`
- **playbooks_prompt_a:** `playbooks_prompt_a`
- **playbooks_prompt_b:** `playbooks_prompt_b`
- **operational_context:** `operational_context`
- **source_artifacts:** `publish_source_artifacts`
- **relationship_links:** `relationship_links`
- **canonical_images:** `publish_canonical_images`

## Demo prompt retrieval checks

### AGVs stopped (prompt_1)
- Expected case: `228086`
- Expected case in top 3: **True**
- `playbook_incident_228086_site_stoppage_optisweep_recovery` case=228086 overlap=0.636 mode=playbook_prompt_b
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery` case=228086 overlap=0.545 mode=playbook_prompt_a
- `playbook_incident_218550_bagout_agv_sequence_recovery` case=218550 overlap=0.455 mode=playbook_prompt_a

### Zone cannot pair (prompt_2)
- Expected case: `228723`
- Expected case in top 3: **True**
- `playbook_incident_228723_zone_pairing_hospitalized_amrs` case=228723 overlap=0.917 mode=playbook_prompt_a
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check` case=228723 overlap=0.917 mode=playbook_prompt_b
- `playbook_incident_218550_bagout_agv_sequence_recovery` case=218550 overlap=0.417 mode=playbook_prompt_a

## Playbook → runbook links (orchestration)

- `playbook_incident_218550_bagout_agv_sequence:node_1` → `proc_identify_whether_an_agv_fault_matches_the_documented_bump_fault_exception_codes_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence:node_1` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 2, None)
- `playbook_incident_218550_bagout_agv_sequence:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 3, None)
- `playbook_incident_218550_bagout_agv_sequence:node_2` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence:node_2` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 2, None)
- `playbook_incident_218550_bagout_agv_sequence:node_2` → `proc_determine_whether_agv_or_rms_is_responsible_for_observed_robot_behavior_v1` (rank 3, None)
- `playbook_incident_218550_bagout_agv_sequence:node_4` → `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence:node_5` → `proc_verify_agvs_are_in_the_szonestaging_state_on_the_hmi_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence:node_5` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_218550_bagout_agv_sequence:node_5` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_1` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 2, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_1` → `proc_interpret_shutdown_queue_behavior_and_agv_movement_during_shutdown_and_startup_v1` (rank 3, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_2` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_2` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 2, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_2` → `proc_interpret_agv_obstacle_alarm_visibility_in_rms_v1` (rank 3, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_4` → `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_4` → `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (rank 2, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_5` → `proc_remove_a_faulted_motionless_agv_from_the_floor_and_restore_operation_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_6` → `proc_verify_agvs_are_in_the_szonestaging_state_on_the_hmi_v1` (rank 1, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_6` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_218550_bagout_agv_sequence_recovery:node_6` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 3, None)
- `playbook_incident_218550_hospital_hmi_fault:node_1` → `proc_review_active_alarms_on_the_hospital_hmi_alarms_screen_v1` (rank 1, None)
- `playbook_incident_218550_hospital_hmi_fault:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_218550_hospital_hmi_fault:node_1` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_218550_hospital_hmi_fault:node_3` → `proc_acknowledge_hospital_hmi_fault_and_retry_hospital_tote_v1` (rank 1, None)
- `playbook_incident_218550_hospital_hmi_fault:node_4` → `proc_review_active_alarms_on_the_hospital_hmi_alarms_screen_v1` (rank 1, None)
- `playbook_incident_218550_hospital_hmi_fault:node_4` → `proc_verify_hospital_hmi_io_diagnostics_input_states_v1` (rank 2, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_1` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 2, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_1` → `proc_distinguish_whether_an_agv_is_in_the_system_versus_in_the_map_v1` (rank 3, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_3` → `proc_recover_empty_agvs_that_lost_tasks_after_rms_restart_v1` (rank 1, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_4` → `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (rank 1, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_5` → `proc_verify_agvs_are_in_the_szonestaging_state_on_the_hmi_v1` (rank 1, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_5` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_5` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 3, None)
- `playbook_incident_223554_agv_tote_state_cleanup:node_6` → `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_1` → `proc_verify_tote_barcode_scan_and_tote_id_population_at_the_hospital_station_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_1` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 3, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_2` → `proc_identify_whether_an_agv_fault_matches_the_documented_bump_fault_exception_codes_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_2` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_2` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_3` → `proc_use_rms_as_a_support_entry_point_to_gather_initial_system_information_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_4` → `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_4` → `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1` (rank 2, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_4` → `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (rank 3, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_5` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_5` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_223554_hospital_induct_blocked_agv_state_recovery:node_5` → `proc_verify_agv_operating_characteristics_and_safety_context_from_training_material_v1` (rank 3, None)
- `playbook_incident_223554_hospital_induct_restore:node_2` → `proc_identify_whether_an_agv_fault_matches_the_documented_bump_fault_exception_codes_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_restore:node_2` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 2, None)
- `playbook_incident_223554_hospital_induct_restore:node_2` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 3, None)
- `playbook_incident_223554_hospital_induct_restore:node_3` → `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_restore:node_4` → `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_restore:node_5` → `proc_identify_why_a_tote_was_sent_to_the_hospital_station_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_restore:node_6` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_223554_hospital_induct_restore:node_6` → `proc_interpret_shutdown_queue_behavior_and_agv_movement_during_shutdown_and_startup_v1` (rank 2, None)
- `playbook_incident_223554_hospital_induct_restore:node_6` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_1` → `proc_review_active_alarms_on_the_hospital_hmi_alarms_screen_v1` (rank 1, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_1` → `proc_check_whether_the_overall_system_rms_page_is_blank_because_rms_access_is_blocked_v1` (rank 2, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 3, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_2` → `proc_identify_control_domains_on_acb_api_screen_v1` (rank 1, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_2` → `proc_shut_down_the_system_from_the_system_api_screen_v1` (rank 2, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_2` → `proc_verify_whether_direct_rms_or_external_api_actions_may_have_bypassed_optisweep_tracking_v1` (rank 3, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_4` → `proc_recover_an_agv_from_a_bump_fault_code_v1` (rank 1, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_5` → `proc_identify_control_domains_on_acb_api_screen_v1` (rank 1, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_5` → `proc_verify_whether_direct_rms_or_external_api_actions_may_have_bypassed_optisweep_tracking_v1` (rank 2, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_5` → `proc_shut_down_the_system_from_the_system_api_screen_v1` (rank 3, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_6` → `proc_interpret_agv_bump_exception_codes_on_the_bump_fault_screen_v1` (rank 1, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_6` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_6` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 3, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_7` → `proc_recover_an_agv_that_lost_a_tote_without_faulting_v1` (rank 1, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_7` → `proc_recover_an_agv_that_lost_a_tote_without_an_agv_fault_v1` (rank 2, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_7` → `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (rank 3, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_8` → `proc_verify_agvs_are_in_the_szonestaging_state_on_the_hmi_v1` (rank 1, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_8` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 2, None)
- `playbook_incident_228086_site_stoppage_optisweep_recovery:node_8` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 3, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_1` → `proc_check_whether_the_overall_system_rms_page_is_blank_because_rms_access_is_blocked_v1` (rank 2, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_1` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_2` → `proc_verify_whether_direct_rms_or_external_api_actions_may_have_bypassed_optisweep_tracking_v1` (rank 1, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_4` → `proc_use_rms_as_a_support_entry_point_to_gather_initial_system_information_v1` (rank 1, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_5` → `proc_recover_an_agv_from_a_bump_fault_code_v1` (rank 1, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_6` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_6` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 2, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_6` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_7` → `proc_recover_an_agv_from_a_bump_fault_code_v1` (rank 1, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_8` → `proc_verify_agvs_are_in_the_szonestaging_state_on_the_hmi_v1` (rank 1, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_8` → `proc_view_current_auv_agv_status_in_the_overall_system_agv_status_pop_up_v1` (rank 2, None)
- `playbook_incident_228086_site_wide_motion_stoppage_service_recovery:node_8` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 3, None)
- `playbook_incident_228086_wcswebapplication_fault_investigation:node_1` → `proc_use_rms_as_a_support_entry_point_to_gather_initial_system_information_v1` (rank 1, None)
- `playbook_incident_228086_wcswebapplication_fault_investigation:node_4` → `proc_use_rms_as_a_support_entry_point_to_gather_initial_system_information_v1` (rank 1, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_1` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_1` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 2, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_1` → `proc_interpret_shutdown_queue_behavior_and_agv_movement_during_shutdown_and_startup_v1` (rank 3, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_3` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_3` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 2, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_3` → `proc_determine_whether_agv_or_rms_is_responsible_for_observed_robot_behavior_v1` (rank 3, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_4` → `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (rank 1, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_5` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_5` → `proc_interpret_shutdown_queue_behavior_and_agv_movement_during_shutdown_and_startup_v1` (rank 2, None)
- `playbook_incident_228723_pairing_failure_hospital_lane_roster_check:node_5` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_228723_zone_pairing_hospitalized_amrs:node_2` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_228723_zone_pairing_hospitalized_amrs:node_2` → `proc_check_whether_the_overall_system_rms_page_is_blank_because_rms_access_is_blocked_v1` (rank 2, None)
- `playbook_incident_228723_zone_pairing_hospitalized_amrs:node_2` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)
- `playbook_incident_228723_zone_pairing_hospitalized_amrs:node_4` → `proc_remove_an_agv_from_the_system_using_the_api_screen_v1` (rank 1, None)
- `playbook_incident_228723_zone_pairing_hospitalized_amrs:node_5` → `proc_check_overall_system_rms_for_system_faults_and_active_agv_faults_v1` (rank 1, None)
- `playbook_incident_228723_zone_pairing_hospitalized_amrs:node_5` → `proc_check_whether_the_overall_system_rms_page_is_blank_because_rms_access_is_blocked_v1` (rank 2, None)
- `playbook_incident_228723_zone_pairing_hospitalized_amrs:node_5` → `proc_interpret_system_faults_versus_agv_system_faults_on_the_overall_system_rms_page_v1` (rank 3, None)

## Validation summary

- Stage 9 status: **passed**
- Errors: 0
- Warnings: 125

## Relationship link quality

- Total links: 17619
- Shared-artifact inferred: 10583
- Needs SME review: 17619

## SME sign-off checklist

- [ ] Confirm Prompt A playbooks route demo prompts 1-2 better than Prompt B where expected.
- [ ] Review all playbook_runbook edges before trusting orchestration.
- [ ] Treat context_runbook_shared_artifact links as hints only unless confidence is high.
- [ ] Spot-check operational_context and source_artifact RAG text for noise before enabling broad retrieval.
- [ ] Sign off publish_version_id before app points at this corpus.
