#!/usr/bin/env python3
import aws_cdk as cdk
from cruise_agent_cdk.core_stack import CoreStack
from cruise_agent_cdk.app_stack import AppStack

app = cdk.App()

core = CoreStack(app, "CruiseAgentCoreStack")
AppStack(app, "CruiseAgentAppStack", core_stack=core)

app.synth()