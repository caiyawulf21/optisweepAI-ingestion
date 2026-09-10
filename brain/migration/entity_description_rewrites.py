"""Hand-written entity description rewrites: entity_id -> corrected description.

Each strips the source-attribution frame ("The manual defines...", "The
training segment describes...") and states the fact directly, preserving
every piece of real content from the original. See BRAIN_BUILD_PROCESS.md
§6.7 for why these are hand-written rather than mechanically generated:
strip_source_reference_leak() only safely handles "The X states that Y" ->
"Y"; the "The X describes Y as Z" -> "Y is Z" shape that dominates this
corpus needs real sentence restructuring a regex cannot do without risking
a grammatically broken result.

This is a PERMANENT, re-appliable fixture, not a one-time patch: a fresh
Pass 0 -> Pass 1 -> consolidate -> Pass 1 rebuild reproduces the exact same
82 entities with the exact same leaked descriptions (deterministic IDs from
unchanged source data), so this file's rewrites need to be re-applied via
cleanup_entity_descriptions.py --apply-hand-rewrites after every fresh
rebuild, the same way reclassify_ambiguous_entities.py does for the 35
reclassified entities. If new leaked descriptions appear (a new source is
migrated, or a schema/migration change surfaces new records), extend this
dict rather than writing a new one-off script.
"""

REWRITES = {
    "entity:component:safety_signal_words_and_symbols":
        "Four safety signal words (DANGER, WARNING, CAUTION, NOTICE) and an electrical hazard symbol are used to alert operators to personal safety and equipment handling risks.",
    "entity:component:operator_safety_responsibility":
        "Operators must read and understand the manual before operating the conveyor. The user is solely responsible for complying with all applicable safety laws and site-specific standards.",
    "entity:system:optisweep_o_m_manual_scope":
        "The manual pertains exclusively to the FORTNA Inc. OptiSweep system.",
    "entity:ui_screen:visu_mancontrol_screen_overview":
        "The VISU_MANCONTROL screen is an Operator Station HMI screen that provides manual controls for the OptiSweep system. The view shown is what personnel logged in as maintenance will see.",
    "entity:ui_screen:hospital_hmi_manual_control_access":
        "The Manual Control function (2.1) is accessible from the Hospital HMI Maintenance Menu.",
    "entity:alarm:alarm_table_structure":
        "Alarms are defined using a table with columns for Text List, ID, Alarm Text, Cause, Controller Response, and Corrective Action.",
    "entity:component:agvs_lost_tasks_recovery_procedure_reference":
        "A fault recovery procedure exists for when empty AGVs lose their tasks after an RMS restart. The procedure involves E-stopping RMS, removing and re-adding AGVs twice, ensuring they are in 'szonestaging' state, and resuming RMS.",
    "entity:component:faulted_agv_with_tote_recovery_concept":
        "A recovery concept exists for a faulted AGV carrying a tote on the RMS: stop the RMS, remove the AGV, take the tote to the Hospital for manual removal, re-add the AGV, and resume the RMS.",
    "entity:component:agv_fault_during_exchange_recovery_concept":
        "A recovery concept exists for when an AGV faults during an exchange on the RMS: stop the RMS, remove the faulted AGV, and potentially introduce a new tote and empty AGV at the location.",
    "entity:component:agv_lost_tote_no_fault_recovery_concept":
        "A recovery concept exists for an AGV that has lost a tote but has not faulted: stop the RMS, manually move the AGV to the Hospital for a system reset, and re-introduce the lost tote.",
    "entity:component:tipper_inspection_checklist_reference":
        "A Tipper Inspection Checklist exists on page 209 of the manual and should be used during tipper inspections to avoid missing important tasks.",
    "entity:system:optisweep_training_session_identification":
        "An introductory title slide identifies a UPS/FORTNA OptiSweep training session labeled Day 1.",
    "entity:component:pre_session_room_and_attendance_logistics":
        "Informal discussion about attendee availability, audio check, Wi-Fi access, and room conditions occurs before the training begins.",
    "entity:component:traditional_small_sort_bagging_operating_model":
        "A traditional small sort bagging system is operator-intensive, with operators assigned destination sections on a sorter and manually handling full bags.",
    "entity:component:belted_acb_solution_bag_flow_description":
        "In a belted ACB solution, a full destination bin is dropped onto a takeaway conveyor and conveyed as a slug to a chute and bag station.",
    "entity:component:optisweep_modularity_and_existing_sorter_adaptation":
        "The OptiSweep design goal is modularity and adaptation to existing building sorters with minimal modification.",
    "entity:system:optisweep_software_as_the_integration_layer":
        "OptiSweep software is the component that integrates multiple subsystems so they communicate and operate together.",
    "entity:system:geek_agv_and_rms_control_architecture_overview":
        "Geek+ AGVs operate over QR codes and are directly controlled by Geek+ RMS, with RMS serving as the robot management layer that handles movement execution and route determination.",
    "entity:component:agv_safety_related_operating_characteristics":
        "AGVs have forward collision sensors and are intended to operate in a fenced system.",
    "entity:component:tote_racking_overview":
        "Tote racks are the structure where the tote sits on the cylinder within the OptiSweep system.",
    "entity:system:tipper_station_overview_at_operator_stations":
        "Each operator station has two tippers used to receive a tote from an AGV, clamp it, tip contents onto a chute, and return the tote.",
    "entity:component:emergency_stop_presence_at_tipper_operation":
        "An operator E-stop is part of the tipper station setup.",
    "entity:system:optisweep_software_environment_overview":
        "The main software elements around OptiSweep are: OptiSweep software as the integrating layer, AVEVA as the HMI, Ignition as the OPC server, Chat XLE for UPS communications, and S-Tunnel for secure connectivity between the OT network and the UPS network.",
    "entity:component:agv_startup_and_shutdown_state_behavior":
        "AGVs are positioned and state-labeled at the beginning and end of a sort cycle.",
    "entity:component:bulk_sort_and_bag_out_functions":
        "The main sorting phase is distinct from the bag-out phase, each with its own role for AGVs and tippers.",
    "entity:system:parcel_lifecycle_into_the_sorter":
        "The upstream parcel flow before and at sorter induction includes unloading from trailers, movement on belts, and arrival onto the sorter with associated data messages.",
    "entity:component:first_chat_message_parcel_data":
        "An initial message from Chat is triggered before sorter entry and carries core parcel attributes.",
    "entity:component:tote_exchange_operating_concept":
        "In an AGV tote exchange, one AGV moves out while another moves in so the exchange happens simultaneously.",
    "entity:metric:chute_opening_timing_and_kpi_emphasis":
        "Chute opening timing is linked to exchange speed: the chute is opened when the AGV moves in rather than when it drops a tote, in support of strict KPI targets.",
    "entity:system:tipper_assignment_and_entrance_queue_concept":
        "A full tote on an AGV is assigned to a tipper and routed through a tipper entrance queue using round-robin selection among available enabled tippers serviced by the queue.",
    "entity:component:tip_staging_notification_and_controller_interface":
        "The handoff between AGV movement and the tipper controller includes AGV travel to the tip location and software notification over OPC that the AGV has staged for a tip.",
    "entity:component:tipper_queue_and_post_tip_flow":
        "Tipper A and tipper B are separate tip locations, each with its own tipper queue. After tipping, an AGV proceeds into the next part of the flow associated with the hospital area.",
    "entity:system:rms_home_screen_navigation_overview":
        "RMS home screen navigation elements include language selection, a collapsible sidebar menu, and access to the Map Monitor view.",
    "entity:ui_screen:map_overview_provides_a_system_level_view":
        "A clickable map overview gives an overview of the system and is used to visually separate major areas such as sorter, charger, and tipper sides.",
    "entity:ui_screen:map_monitor_message_panel_overview":
        "A Map Monitor message panel on the right side of the interface lists several robot and AGV status and fault-related items.",
    "entity:ui_screen:robot_restart_panel_and_selection_inputs":
        "A restart panel lets an operator enter a robot ID or select a robot, then use a Restart control to restart that robot.",
    "entity:component:task_persistence_across_restart_versus_removal":
        "A robot's transaction resumes after restart unless the robot is removed from the system.",
    "entity:ui_screen:rack_locations_in_the_rms_map_view":
        "Rack locations are selectable map elements in the RMS/container selection view, used to inspect rack-specific information.",
    "entity:state:rack_color_indicates_tote_presence_state":
        "Two rack colors are used in the map view: dark blue/violet indicates a tote is present, and light blue indicates the rack is empty.",
    "entity:ui_screen:robot_selection_restart_screen_reference":
        "A Robot Selection Restart screen is used to identify a robot by robot ID or selection and initiate a restart.",
    "entity:ui_screen:container_selection_screen_overview":
        "A Container Selection screen is used to view totes or containers, associated rack locations, and related identifiers within the system.",
    "entity:state:container_color_indicators_on_the_screen":
        "Color coding indicates whether a rack location contains a tote.",
    "entity:ui_screen:agv_object_selection_displays_agv_specific_information":
        "Selecting an AGV object in the interface causes AGV information to display.",
    "entity:component:overall_system_bag_out_control":
        "Overall system bag out is a control concept that closes destinations and exchanges totes containing parcels.",
    "entity:component:pre_bag_out_exchange_scope":
        "Pre bag out exchanges the lowest 25 percent of destinations per sorter leg.",
    "entity:ui_screen:overall_system_agv_status_popup_overview":
        "An AGV status popup presents detailed information for AGVs in the overall system view.",
    "entity:component:hot_bin_behavior_in_optisweep":
        "Hot bins are bins associated with totes marked for hot bin handling, causing chute close and exchange behavior.",
    "entity:ui_screen:api_page_overview_in_aveva":
        "An Aveva page referred to as the API page exposes system-level OptiSweep functions through APIs and is shown on the left side of the system display.",
    "entity:component:system_bag_out_close_out_concept":
        "Close out, associated with System Bag Out, closes all chutes and exchanges totes with items at the end of a sort, with labels printed for totes with items.",
    "entity:metric:reset_metrics_behavior":
        "Metrics are reset automatically when a new sort plan is loaded, and can also be manually reset from the Reset Metrics control.",
    "entity:ui_screen:initialize_tote_aveva_api_page_overview":
        "An Aveva API page is used to initialize a tote for processing in the system.",
    "entity:symptom:repeat_incident_avoidance_as_a_training_concept":
        "Avoidance of repeated occurrence of the same issue is an important troubleshooting-related concept.",
    "entity:system:overall_system_statistics_overview":
        "An Overall System Statistics area contains Main Statistics and core system statistics.",
    "entity:metric:e_stop_statistics_as_a_statistics_type":
        "E-stop is one of the statistics types available within the Overall System Statistics view.",
    "entity:metric:types_of_customer_defined_calculations":
        "There are three types of customer-defined calculations: system statistics, bin statistics, and tipper statistics.",
    "entity:ui_screen:overall_system_rms_screen":
        "An Overall System RMS page is associated with the Geek+ RMS web page.",
    "entity:ui_screen:overall_system_agv_status_page":
        "An HMI page is titled \"Overall System AGV Status.\"",
    "entity:ui_screen:auv_status_pop_up_screen":
        "An AUV status pop-up provides detailed status information.",
    "entity:system:fortna_optisweep_training_day_2":
        "An introductory training video segment covers FORTNA OptiSweep Training - Day 2.",
    "entity:component:training_video_recording_provenance":
        "The recording date and named organizers or contributors are identified.",
    "entity:component:database_walkthrough":
        "The segment is titled \"Database Walkthrough.\"",
    "entity:system:database_walkthrough_training_slide":
        "A Day 2 training slide titled \"Database Walkthrough\" marks the segment's subject area.",
    "entity:system:optisweep_robotics_database_landscape":
        "The robotics database environment consists of multiple databases rather than a single system database.",
    "entity:system:sorter_database_model_overview":
        "The sorter database model is an overview of storage data, relationships, configuration, activities, and foreign-key connections.",
    "entity:metric:sys1_metric_to_tag_conversion":
        "SYS1 is the location where metrics are converted into tags for AVEVA to read.",
    "entity:symptom:crash_example":
        "An example of a crash is presented.",
    "entity:metric:memory_trend_and_garbage_collection_behavior":
        "A Memory Trend display shows memory usage over time, including increases, drops, and periods of little or no activity attributed to garbage collection.",
    "entity:component:windows_service_and_log_visibility":
        "Windows service administration and logs are places where service state or activity may be visible.",
    "entity:state:services_status_reference":
        "The Services interface represents whether relevant services are up and running.",
    "entity:component:sql_server_management_studio_connection_reference":
        "SQL Server Management Studio is the database connectivity interface used.",
    "entity:state:services_and_unplanned_restart_context":
        "Windows services and an unplanned restart are associated with the FORTNA WCS primary host context.",
    "entity:state:heartbeat_flatline_indication":
        "A flatlined heartbeat is an indication associated with delayed startup of Ignition services relative to WCS and OptiSweep.",
    "entity:component:optisweep_windows_service_reference":
        "OptiSweep appears as a Windows service in the Services console, with service status and startup configuration fields visible.",
    "entity:ui_screen:rms_monitor_and_robot_control_screen":
        "An RMS screen at the monitor/robotControl path has a loading state relevant to diagnostics.",
    "entity:role:rms_administrator_access":
        "An RMS access notation of \"C: admin +\" indicates an administrator-related access context.",
    "entity:component:master_e_stop_and_ups_reference":
        "A UPS and a master E-stop are referenced in the context of an unplanned restart and RMS screen availability.",
    "entity:component:remote_access_to_the_computer":
        "The computer can be accessed remotely.",
    "entity:component:sql_server_agent_service":
        "SQL Server Agent is a service associated with RMS operation; its running state is checked in SQL Server Configuration Manager.",
    "entity:ui_screen:sql_server_configuration_manager_service_view":
        "The SQL Server Configuration Manager local services view includes SQL Server, SQL Server Agent, SQL Server Browser, and related configuration categories.",
    "entity:symptom:unplanned_restart_and_job_cleanup_issue":
        "An earlier unplanned restart is associated with SQL Server Agent jobs not cleaning up expected items.",
    "entity:ui_screen:mdi_support_chat_package_data_view":
        "An MDI Support chat view for Haslet contains package-level classification and sort-related data.",
    "entity:system:expected_dimension_data_from_dimensioners":
        "Dimension data from the dimensioners is data expected by the OptiSweep-related support view or system.",
}
