import type { BasicAPI } from '@/services/site-data/typings';
import request from 'umi-request';

export const websiteBasicData = async (options?: Record<string, any>) =>
  request<BasicAPI.basicData>('/main/api/v2/get_website_info', {
    method: 'GET',
    ...(options || {}),
  });

export const projectRuntime = async () =>
  request<BasicAPI.projectRuntimeData>('/main/api/v2/get_project_runtime', {
    method: 'GET',
  });

export const knowledgeExtract = async (body: BasicAPI.rawKnowledgeMessageParams) =>
  request<BasicAPI.rawKnowledgeMessageResults>('main/api/v2/extractKnowledge', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
  });

export const startBuildSandbox = async (body: BasicAPI.startBuildSandbox) =>
  request<BasicAPI.startBuildSandboxResult>('main/api/v2/build_sandbox', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
  });

export const buildingPolling = async (task_id: string) =>
  request<BasicAPI.buildingPollingResult>(`/main/api/v2/status/${task_id}`, {
    method: 'GET',
  });
