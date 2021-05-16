import type { ColumnsType } from 'antd/es/table';

declare namespace ProjectApi {
  type singleRuntime = {
    create_date_time: string;
    update_date_time: string;
    s_project_description: string;
    login_name: string;
    s_project_name: string;
    status: string;
    mark: string;
    badge_color: string;
    analyse_type: number;
    current_step: number;
    total_step: number;
  };
  type runtimeResult = {
    running: singleRuntime[];
    creating: singleRuntime[];
    exited: singleRuntime[];
    deleted: singleRuntime[];
  };
  type projectDetailResult = {
    create_date_time: string;
    update_date_time: string;
    s_project_description: string;
    login_name: string;
    s_project_name: string;
    status: string;
    mark: string;
    badge_color: string;
    analyse_type: number;
    current_step: number;
    total_step: number;
    data: any;
    labels: [];
    remark: {
      port: string;
      password: string;
    };
  };
  type normalOperatorResult = {
    msg: string;
    code?: number;
  };
  type getSqlDataBody = {
    'db-host': string;
    'db-port': string;
    'db-username': string;
    'db-password': string;
    'db-database': string;
  };
  type getSqlDataResult = {
    msg?: string;
    code?: number;
    data: [
      {
        table_name: string;
        data: [];
        columns: ColumnsType<Record<string, string>>;
      },
    ];
  };
  type getJsonBody = {
    data: [];
  };
  type getJsonResult = any;
  type singleNode = {
    name: string;
    type: string;
  };
  type singleResult = {
    nodes: singleNode[];
    relationships: [];
  };
  type buildSandboxViaStructDataBody = {
    data: singleResult;
    projectName: string;
    needEmail: boolean;
    projectDescription: string;
  };
  type buildSandboxViaStructDataResult = {
    task_id: string;
  };
}
