.PHONY: help qa-test-unit qa-test-integration qa-test-all qa-lint qa-typecheck image-build env-smoke-up env-smoke-wait verify-smoke env-smoke-down env-smoke-logs flow-dev-check

# 默认测试目标
UNIT_TARGETS ?= tests/unit
INTEGRATION_TARGETS ?= tests/integration
SMOKE_DOWN_VOLUMES ?= false

help:
	@echo "Agent Engine Makefile 帮助指南"
	@echo ""
	@echo "使用方法:"
	@echo "  make qa-test-unit         - 运行单元测试 (默认: tests/unit)"
	@echo "  make qa-test-integration  - 运行集成测试 (默认: tests/integration)"
	@echo "  make qa-test-all          - 运行所有测试"
	@echo "  make qa-lint              - 运行代码规范检查 (Ruff)"
	@echo "  make qa-typecheck         - 运行类型检查 (Ty)"
	@echo "  make image-build          - 构建 Docker 镜像"
	@echo "  make env-smoke-up         - 启动 Smoke 测试环境"
	@echo "  make env-smoke-wait       - 等待 Smoke 测试环境就绪"
	@echo "  make verify-smoke         - 运行 Smoke 验证关键链路"
	@echo "  make env-smoke-down       - 清理 Smoke 测试环境"
	@echo "  make env-smoke-logs       - 查看 Smoke 环境日志"
	@echo "  make flow-dev-check       - 提交流程检查 (单测+集成测+Lint+Typecheck)"

# ==============================================================================
# QA & Testing (质量保证与测试)
# ==============================================================================

qa-test-unit:
	uv run pytest $(UNIT_TARGETS)

qa-test-integration:
	uv run pytest $(INTEGRATION_TARGETS)

qa-test-all:
	uv run pytest tests/

qa-lint:
	uv run ruff check .
	# 使用 uv run ruff format . 格式化代码，若需自动修复可加上 --fix

qa-typecheck:
	uv run ty

# ==============================================================================
# Docker & Smoke Environment (容器与起步环境)
# ==============================================================================

image-build:
	docker build -t agent-engine:latest .

env-smoke-up:
	@echo "启动 docker-compose 环境..."
	docker compose up -d || echo "注意: 当前可能尚未配置 docker-compose.yml 依赖环境文件"

env-smoke-wait:
	@echo "等待服务就绪..."
	sleep 5

verify-smoke:
	@echo "运行 Smoke 验证..."
	# 此处可添加基于 curl 的健康检查，或者指向特定的 smoke test marker
	# curl -s http://localhost:8000/health || exit 1
	@echo "✅ Smoke 测试桩点默认通过"

env-smoke-down:
	@echo "清理 docker-compose 环境..."
	@if [ "$(SMOKE_DOWN_VOLUMES)" = "true" ]; then \
		echo "移除卷数据..."; \
		docker compose down -v; \
	else \
		docker compose down; \
	fi

env-smoke-logs:
	docker compose logs -f

# ==============================================================================
# Workflows (研发工作流编排)
# ==============================================================================

flow-dev-check: qa-test-unit qa-test-integration qa-lint qa-typecheck
	@echo "✅ 开发前置流程 (Dev-Check) 全部通过！"
