import { request } from '@@/plugin-request/request';
import type { ProjectApi } from '@/services/projects-operator/typing';

/**
 * 获取服务器端的各个容器的状态信息
 */
export const projectsRuntime = async () =>
  request<ProjectApi.runtimeResult>('/main/api/v2/get_project_runtime', {
    method: 'GET',
  });

/**
 * 获取项目的详情信息
 * @param taskId
 */
export const get_project_detail = async (taskId: string) =>
  request<ProjectApi.projectDetailResult>(`/main/api/v2/show_project_detail/${taskId}`, {
    method: 'GET',
  });

/**
 * 停止项目容器
 * @param taskId
 */
export const project_deleted = async (taskId: string) =>
  request<ProjectApi.normalOperatorResult>(`/main/api/v2/delete_project/${taskId}`, {
    method: 'DELETE',
  });

/**
 * 启动项目容器
 * @param taskId
 */
export const project_start = async (taskId: string) =>
  request<ProjectApi.normalOperatorResult>(`/main/api/v2/start_project/${taskId}`, {
    method: 'GET',
  });

/**
 * 休眠项目容器
 * @param taskId
 */
export const project_exited = async (taskId: string) =>
  request<ProjectApi.normalOperatorResult>(`/main/api/v2/exited_project/${taskId}`, {
    method: 'PUT',
  });

/**
 * 获取结构化数据以进行数据校验
 * @param body
 */
export const getSqlData = async (body: ProjectApi.getSqlDataBody) =>
  request<ProjectApi.getSqlDataResult>('/main/api/v2/knowledge_extract_from_database', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
  });

/**
 * 从结构化数据构建sandbox
 * @param body
 */
export const buildSandboxViaStructData = async (body: ProjectApi.buildSandboxViaStructDataBody) =>
  request<ProjectApi.buildSandboxViaStructDataResult>(
    '/main/api/v2/build_sandbox_via_struct_data',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      data: body,
    },
  );

export const getJsonData = async (body: ProjectApi.getJsonBody) =>
  request<ProjectApi.getJsonResult>('/main/api/v2/knowledge_extract_from_json', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
  });
