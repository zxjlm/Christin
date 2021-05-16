import { Divider, List, message, Modal, Popover, Space, Switch, Tag } from 'antd';
import {
  ProFormText,
  ProFormTextArea,
  ProFormUploadDragger,
  StepsForm,
} from '@ant-design/pro-form';
import { waitTime } from '@/utils/useful';
import Title from 'antd/es/typography/Title';
import Paragraph from 'antd/es/typography/Paragraph';
import Text from 'antd/es/typography/Text';
import { useState } from 'react';
import { buildSandboxViaStructData, getJsonData } from '@/services/projects-operator/api';
import { typeColorMapper } from '@/components/ProjectDetail';
import { ExclamationCircleOutlined } from '@ant-design/icons';
import { openNotification } from '@/components/InputStepForms/NormalStepForm';
import PollStopCard from '@/components/PollStopCard';

const { confirm } = Modal;

export default () => {
  const [projectInfo, setProjectInfo] = useState({
    projectName: 'undefined',
    projectDescription: '',
  });
  const [entsData, setEntsData] = useState<{ s_name: string; type: string }[]>([]);
  const [needEmail, setNeedEmail] = useState(true);
  const [formHash, setFormHash] = useState('');
  const [taskId, setTaskId] = useState<string | undefined>(undefined);
  const [startPolling, setStartPolling] = useState(false);

  const stepOneFinish = async (formData: Record<string, any>) => {
    const postData = formData['json-files']
      .filter((item: { status: string }) => item.status === 'done')
      .map((item: { response: any }) => item.response.data);
    getJsonData(postData.flat())
      .then((response) => {
        setEntsData(response.data);
        setProjectInfo({
          projectName: formData['project-name'],
          projectDescription: formData['project-description'],
        });
      })
      .catch((response) => {
        message.warning(response.msg);
        return false;
      });
    return true;
  };

  const stepTwoFinish = async () => {
    const validateEnts = {
      nodes: entsData.map((item) => ({ name: item.s_name, ...item })),
      relationships: [],
    };
    const postData: any = {
      projectName: projectInfo.projectName,
      projectDescription: projectInfo.projectDescription,
      data: validateEnts,
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

  const closeTagHandler = (e: any) => {
    const name = e.target.parentNode.parentNode.parentNode.innerText;
    e.preventDefault();

    confirm({
      title: 'Do you Want to delete these items?',
      icon: <ExclamationCircleOutlined />,
      onOk() {
        setEntsData(entsData.filter((item) => item.s_name !== name));
      },
      onCancel() {
        console.log('Cancel');
      },
    });
  };

  const entPropertiesList = (node: Record<string, string>) => (
    <List
      size="small"
      dataSource={Object.entries(node)}
      renderItem={(item) => (
        <List.Item>
          {item[0]} : {item[1]}
        </List.Item>
      )}
    />
  );

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
        <Title level={2}>
          半结构化数据录入说明(<Text type={'danger'}> 开发中</Text>)
        </Title>
        <Paragraph>
          半结构化数据录入目前主要针对的是JSON类型的数据,总共分为<Text mark>三步</Text>.
        </Paragraph>
        <Title level={3}>第一步: 数据录入</Title>
        <Paragraph>
          数据录入需要输入 <Text mark>项目名称 项目描述 待提取数据</Text> 三个基本信息, 其中,
          项目名称与待提取数据为必填项.
        </Paragraph>
        <Paragraph>
          待提取数据为json文件, 并且内容必须符合json的范式, 平台会进行文件内容校验并按照{' '}
          <Text mark>映射逻辑</Text> 进行数据抽取{' '}
        </Paragraph>
        <Title level={3}>第二步: 审核表单</Title>
        <Paragraph>
          平台在会抽取提取到的<Text type={'success'}>一部分</Text> 数据返回并进行数据核验
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
      <StepsForm.StepForm name="base" title="数据录入" onFinish={stepOneFinish}>
        <div style={{ marginLeft: '30px' }}>
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
        </div>
        <ProFormUploadDragger
          max={4}
          name="json-files"
          title={'从JSON文件导入'}
          description={'目前只支持中药数据'}
          accept={'.json'}
          action={'/main/api/v2/extract_from_json'}
        />
      </StepsForm.StepForm>
      <StepsForm.StepForm name="checkbox" title="审核数据" onFinish={stepTwoFinish}>
        {Object.entries(typeColorMapper).map((item) => (
          <Tag key={item[0]} color={item[1]}>
            {item[0]}
          </Tag>
        ))}
        <Divider />
        <Title level={2}>解析结果</Title>
        <Space direction="vertical" style={{ marginBottom: '50px' }}>
          {entsData.map((node) => (
            <Popover
              content={entPropertiesList(node)}
              title={node.s_name}
              key={node.s_name}
              placement={'right'}
            >
              <Tag color={typeColorMapper[node.type]} closable={true} onClose={closeTagHandler}>
                {node.s_name}
              </Tag>
            </Popover>
          ))}
        </Space>
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
