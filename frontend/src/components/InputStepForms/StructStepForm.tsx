import { StepsForm, ProFormText, ProFormTextArea } from '@ant-design/pro-form';
import { Divider, message, Switch, Table } from 'antd';
import { buildSandboxViaStructData, getSqlData } from '@/services/projects-operator/api';
import { useState } from 'react';
import type { ProjectApi } from '@/services/projects-operator/typing';
import PollStopCard from '@/components/PollStopCard';
import { openNotification } from '@/components/InputStepForms/NormalStepForm';
import Title from 'antd/es/typography/Title';
import Paragraph from 'antd/es/typography/Paragraph';
import Text from 'antd/es/typography/Text';

const waitTime = (time: number = 100) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true);
    }, time);
  });
};

export default () => {
  const [projectInfo, setProjectInfo] = useState({
    projectName: 'undefined',
    projectDescription: '',
  });
  const [needEmail, setNeedEmail] = useState(true);
  const [responseData, setResponseData] = useState<ProjectApi.getSqlDataResult>({
    code: 0,
    data: [{ columns: [{ title: '', dataIndex: '' }], data: [], table_name: '' }],
    msg: '',
  });
  const [taskId, setTaskId] = useState<string | undefined>(undefined);
  const [startPolling, setStartPolling] = useState(false);
  const [formHash, setFormHash] = useState('');

  const stopOneFinish = async (formData: any) => {
    getSqlData(formData).then((response) => {
      setProjectInfo({
        projectName: formData['project-name'],
        projectDescription: formData['project-description'],
      });
      setResponseData(response);
    });
    return true;
  };

  const stopTwoFinish = async () => {
    const pre_nodes: any = responseData.data.map((item) => ({
      nodes: [
        item.data.map((node: any) => ({
          name: node.s_name,
          type: item.table_name.replace('tb_', '').toUpperCase(),
          ...node,
        })),
      ],
      relationship: [],
    }));
    let result_nodes: any = [];
    pre_nodes.forEach((item: { nodes: any }) => {
      result_nodes = result_nodes.concat(item.nodes[0]);
    });
    const postData: ProjectApi.buildSandboxViaStructDataBody = {
      projectName: projectInfo.projectName,
      projectDescription: projectInfo.projectDescription,
      data: { nodes: result_nodes, relationships: [] },
      needEmail,
    };
    if (formHash !== JSON.stringify(postData)) {
      buildSandboxViaStructData(postData).then((response) => {
        setTaskId(response.task_id);
        setFormHash(JSON.stringify(postData));
      });
    } else {
      openNotification('表单未曾发生改变, 默认不进行提交');
      setStartPolling(!startPolling);
    }
    return true;
  };

  return (
    <StepsForm
      onFinish={async (values) => {
        console.log(values);
        await waitTime(1000);
        message.success('提交成功');
      }}
      formProps={{
        validateMessages: {
          required: '此项为必填项',
        },
      }}
    >
      <StepsForm.StepForm
        name="instruction"
        title="说明"
        onFinish={async () => {
          await waitTime(1000);
          return true;
        }}
      >
        <Title level={2}>结构化数据录入说明</Title>
        <Paragraph>
          结构化数据录入目前主要针对的是MySQL类型的数据,总共分为<Text mark>三步</Text>.
        </Paragraph>
        <Title level={3}>第一步: 数据录入</Title>
        <Paragraph>
          数据录入需要输入 <Text mark>项目名称 项目描述 数据库配置</Text> 三个基本信息, 其中,
          项目名称与数据库配置为必填项.
        </Paragraph>
        <Paragraph>
          在数据库配置中, 需要输入数据库的ip\端口\用户名\密码\数据库名,
          平台会按照配置检索到对应的数据库并按照 <Text mark>表映射逻辑</Text> 进行数据抽取{' '}
        </Paragraph>
        <Paragraph>
          ps1. 不要使用<Text type={'danger'}>本地的(localhost\127.0.0.1)</Text>数据库, 以及{' '}
          <Text type={'danger'}>任何外网无法访问</Text> 的数据库{' '}
        </Paragraph>
        <Paragraph>
          ps2. 将网站ip添加至数据库的 <Text type={'warning'}> 远程信任名单</Text>
        </Paragraph>
        <Title level={3}>第二步: 审核表单</Title>
        <Paragraph>
          平台在会抽取数据库的<Text type={'success'}> 一部分</Text> 数据返回并进行数据核验
        </Paragraph>
        <Title level={3}>第三步: 构建图数据库</Title>
        <Paragraph>
          图数据库的构建全程由平台的自动化系统完成, 用户
          <Text type={'success'}> 不需要保持网页焦点</Text> , 在图数据库构建完成后, 会进行邮件通知{' '}
          <Text type={'secondary'}>(如果选择了邮件通知的话)</Text>.{' '}
        </Paragraph>
        <Paragraph>
          最后, 用户可以通过网站ip的 <Text code>7474</Text>端口进行neo4j原生浏览器访问, 或者根据{' '}
          <Text mark>项目信息页面提供的链接</Text> 访问网站自开发的图数据库可视化系统.
        </Paragraph>
      </StepsForm.StepForm>
      <StepsForm.StepForm name="base" title="数据录入" onFinish={stopOneFinish}>
        <ProFormText
          name="project-name"
          label="项目名称"
          width="md"
          tooltip="最长为 24 位，用于标定的唯一 id"
          placeholder="请输入项目名称"
          rules={[{ required: true }]}
        />
        <ProFormTextArea
          name="project-description"
          label="项目描述"
          width="lg"
          placeholder="请输入项目描述(250字以内)"
          initialValue={'无'}
        />
        <ProFormText
          name="db-host"
          label="ip地址"
          width="md"
          placeholder="请输入数据库地址"
          rules={[{ required: true }]}
          initialValue={'localhost'}
        />
        <ProFormText
          name="db-port"
          label="端口"
          width="md"
          placeholder="请输入数据库端口"
          rules={[{ required: true }]}
          initialValue={3306}
        />
        <ProFormText
          name="db-username"
          label="用户名"
          width="md"
          placeholder="请输入数据库用户名"
          rules={[{ required: true }]}
          initialValue={'root'}
        />
        <ProFormText.Password
          name="db-password"
          label="密码"
          width="md"
          placeholder="请输入数据库密码"
          rules={[{ required: true }]}
          initialValue={'root'}
        />
        <ProFormText
          name="db-database"
          label="数据库名"
          width="md"
          placeholder="请输入数据库名称"
          rules={[{ required: true }]}
          style={{ marginBottom: '20px' }}
          initialValue={'Christin'}
        />
      </StepsForm.StepForm>
      <StepsForm.StepForm<{
        checkbox: string;
      }>
        name="checkbox"
        title="审核表单"
        onFinish={stopTwoFinish}
      >
        {responseData.data.map((item) => (
          <div key={Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER))}>
            <h2>{item.table_name}</h2>
            <Table columns={item.columns} dataSource={item.data} pagination={false} />
            <Divider />
          </div>
        ))}
        <div style={{ marginLeft: '30px', marginTop: '10px', marginBottom: '20px' }}>
          <Switch
            checkedChildren={'使用邮件通知'}
            unCheckedChildren={'不需要邮件'}
            defaultChecked={true}
            onChange={(checked) => setNeedEmail(checked)}
          />
        </div>
      </StepsForm.StepForm>
      <StepsForm.StepForm name="time" title="构建图数据库">
        <PollStopCard taskId={taskId} startPolling={startPolling} />
      </StepsForm.StepForm>
    </StepsForm>
  );
};
