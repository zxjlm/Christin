import ProDescriptions from '@ant-design/pro-descriptions';
import type { annotationType } from '@/components/SingleAnnotation';
import SingleAnnotation from '@/components/SingleAnnotation';
import { Button, Card, Divider, Space, Tag } from 'antd';
import type { ProjectApi } from '@/services/projects-operator/typing';
import { history } from 'umi';

export const typeColorMapper = {
  HERB: 'red',
  PRESCRIPTION: 'magenta',
  DISEASE: 'volcano',
  INGREDIENT: 'orange',
  MM_SYMPTOM: 'gold',
  TCM_SYMPTOM: 'lime',
  TARGET: 'cyan',
};

export default ({ projectData }: { projectData: ProjectApi.projectDetailResult }) => {
  const textDataDisplay = () => (
    <Space direction="vertical">
      {projectData.data.map(
        (doc: { annotations: annotationType[]; text: string }, list_id: number) => (
          <Card type="inner" key={Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER))}>
            <SingleAnnotation
              labels={projectData.labels}
              text={doc.text}
              list_id={list_id}
              readOnly={true}
            />
          </Card>
        ),
      )}
    </Space>
  );

  const halfStructDisplay = () => <div>9527</div>;

  const structDisplay = () => (
    <div>
      tags:{' '}
      {Object.entries(typeColorMapper).map((item) => (
        <Tag key={item[0]} color={item[1]}>
          {item[0]}
        </Tag>
      ))}
      <Divider />
      <Space direction="vertical">
        {projectData.data.nodes.map((node: { s_name: string; type: string }) => (
          <Tag color={typeColorMapper[node.type]} key={node.s_name}>
            {node.s_name}
          </Tag>
        ))}
      </Space>
    </div>
  );

  const displayMapper = [structDisplay, halfStructDisplay, textDataDisplay];

  const mainForm = (
    <ProDescriptions column={2} title={projectData.s_project_name} tooltip="项目名称">
      <ProDescriptions.Item span={2} label="项目描述">
        {projectData.s_project_description || '无项目描述'}
      </ProDescriptions.Item>
      <ProDescriptions.Item label="创建日期" valueType="dateTime">
        {Date.parse(projectData.create_date_time)}
      </ProDescriptions.Item>
      <ProDescriptions.Item label="更新日期" valueType="dateTime">
        {Date.parse(projectData.update_date_time)}
      </ProDescriptions.Item>
      <ProDescriptions.Item
        label="项目状态"
        valueEnum={{
          all: { text: '全部', status: 'Default' },
          deleted: {
            text: '已删除',
            status: 'Error',
          },
          running: {
            text: '运行中',
            status: 'Success',
          },
          exited: {
            text: '已退出',
            status: 'Processing',
          },
          creating: {
            text: '创建中',
            status: 'Processing',
          },
        }}
      >
        {projectData.status}
      </ProDescriptions.Item>
      <ProDescriptions.Item label="项目处理进度" valueType="progress">
        100
      </ProDescriptions.Item>
      <ProDescriptions.Item label="密码">{projectData.remark.password}</ProDescriptions.Item>
      <ProDescriptions.Item label="端口">{projectData.remark.port}</ProDescriptions.Item>
      <ProDescriptions.Item label="分析数据">
        {displayMapper[projectData.analyse_type]()}
      </ProDescriptions.Item>
    </ProDescriptions>
  );

  if (projectData.status === 'running') {
    return (
      <div>
        {mainForm}
        <Button
          type={'primary'}
          // href={`http://localhost/christin-graph/${projectData.remark.port}/${projectData.remark.password}`}
          onClick={() =>
            history.push(
              `/graphinneo/graph/${projectData.remark.port}/${projectData.remark.password}`,
            )
          }
          style={{ marginLeft: '45%' }}
        >
          前往数据库
        </Button>
      </div>
    );
  }

  return <div>{mainForm}</div>;
};
