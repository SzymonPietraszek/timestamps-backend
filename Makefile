SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

include build.env
export

AWS_ACCOUNT_ID := $(shell aws sts get-caller-identity --query Account --output text)
ECR_URL := $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
IMAGE_URI := $(ECR_URL)/$(ECR_REPOSITORY)

.PHONY: validate login build push lambda deploy

REQUIRED_VARS := \
	IMAGE_TAG \
	AWS_REGION \
	PLATFORM \
	PYTHON_VERSION \
	ECR_REPOSITORY \
	LAMBDA_FUNCTION_NAME

validate:
	@$(foreach var,$(REQUIRED_VARS), \
		test -n "$($(var))" || { echo "$(var) is required"; exit 1; }; \
	)

login: validate
	aws ecr get-login-password --region $(AWS_REGION) | \
	docker login --username AWS --password-stdin $(ECR_URL)

build: validate
	docker build \
	--platform $(PLATFORM) \
	--provenance=false \
	--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
	-t $(IMAGE_URI):$(IMAGE_TAG) .

push: validate
	docker push $(IMAGE_URI):$(IMAGE_TAG)

lambda: validate
	aws lambda update-function-code \
	--function-name $(LAMBDA_FUNCTION_NAME) \
	--image-uri $(IMAGE_URI):$(IMAGE_TAG)

deploy: login build push lambda
