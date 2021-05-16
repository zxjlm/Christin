import { Button, Col, Divider, Dropdown, Menu, message, Modal, Progress, Row, Tag } from 'antd';
import {
  get_project_detail,
  project_deleted,
  project_exited,
  project_start,
  projectsRuntime,
} from '@/services/projects-operator/api';
import { useEffect, useState } from 'react';
import type { runtimeDataProp } from '@/components/ContainerCard';
import ContainerCard from '@/components/ContainerCard/index';
import ProjectDetail from '@/components/ProjectDetail/index';
import { useModel } from '@@/plugin-model/useModel';
import img1 from '@/images/1.png';
import img2 from '@/images/2.png';
import img3 from '@/images/3.png';
import img4 from '@/images/4.png';
import type { ProjectApi } from '@/services/projects-operator/typing';
import Text from 'antd/es/typography/Text';

const cats = [img1, img2, img3, img4];
const typeMapper = ['结构化数据', '半结构化数据', '非结构化数据'];
const typeColorMapper = ['volcano', 'orange', 'geekblue'];
const statusColorMapper = {
  creating: 'lime',
  running: 'green',
  exited: 'magenta',
  deleted: 'red',
};
const datetimeColorMapper = {
  danger: 'red',
  info: 'blue',
  warning: 'gold',
};

export default () => {
  const initProjectData: ProjectApi.projectDetailResult = {
    badge_color: '',
    create_date_time: '',
    data: [],
    login_name: '',
    mark: '',
    remark: { password: '', port: '' },
    s_project_description: '',
    s_project_name: '',
    status: '',
    labels: [],
    update_date_time: '',
    analyse_type: 0,
    current_step: 4,
    total_step: 4,
  };

  const [projectsRuntimeInfo, setProjectsRuntimeInfo] = useState<ProjectApi.runtimeResult>({
    creating: [],
    deleted: [],
    exited: [],
    running: [],
  });
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [transferData, setTransferData] = useState<ProjectApi.projectDetailResult>(initProjectData);
  const { nerDocs, setNerDocs } = useModel('nerDocs', (model) => ({
    setNerDocs: model.setNerDocs,
    nerDocs: model.nerDocs,
  }));

  const menu = (cardId: string, status: string) => {
    const view = () => {
      get_project_detail(cardId).then((data) => setTransferData(data));
    };

    const deleted = () => {
      message
        .loading('操作中..', 1.5)
        .then(() => project_deleted(cardId))
        .then((response) => message.success(response.msg, 1.5))
        .then(() => {
          projectsRuntime().then((result) => setProjectsRuntimeInfo(result));
        });
    };

    const exited = () => {
      message
        .loading('操作中..', 1.5)
        .then(() => project_exited(cardId))
        .then((response) => message.success(response.msg, 1.5))
        .then(() => {
          projectsRuntime().then((result) => setProjectsRuntimeInfo(result));
        });
    };

    const start = () => {
      message
        .loading('操作中..', 1.5)
        .then(() => project_start(cardId))
        .then((response) => message.success(response.msg, 1.5))
        .then(() => {
          projectsRuntime().then((result) => setProjectsRuntimeInfo(result));
        });
    };

    const view_node = (
      <Menu.Item>
        <a onClick={view}>查看</a>
      </Menu.Item>
    );
    const start_node = (
      <Menu.Item>
        <a onClick={start}>启动</a>
      </Menu.Item>
    );
    const exit_node = (
      <Menu.Item>
        <a onClick={exited}>休眠</a>
      </Menu.Item>
    );
    const delete_node = (
      <Menu.Item>
        <a onClick={deleted}>删除</a>
      </Menu.Item>
    );

    switch (status) {
      case 'creating':
        return (
          <Menu>
            <Menu.Item>
              <Text>创建状态的项目不接受任何操作</Text>
            </Menu.Item>
          </Menu>
        );
      case 'running':
        return (
          <Menu>
            {view_node}
            {exit_node}
          </Menu>
        );
      case 'exited':
        return (
          <Menu>
            {view_node}
            {start_node}
            {delete_node}
          </Menu>
        );
      case 'deleted':
        return <Menu>{view_node}</Menu>;
      default:
        return <Menu>{view_node}</Menu>;
    }
  };

  const parserData = (item: ProjectApi.singleRuntime): runtimeDataProp => ({
    title: item.s_project_name,
    subTitle: <Tag color="purple">{item.login_name}</Tag>,
    type: item.status,
    avatar: cats[Math.floor(Math.random() * cats.length)],
    status: item.status,
    content: (
      <div
        style={{
          flex: 1,
        }}
      >
        <Row>
          <Col span={6}>项目状态:</Col>
          <Col span={10}>
            <Tag color={statusColorMapper[item.status]}>{item.status}</Tag>
          </Col>
        </Row>
        <Row>
          <Col span={6}>项目类型:</Col>
          <Col span={10}>
            <Tag color={typeColorMapper[item.analyse_type]}>{typeMapper[item.analyse_type]}</Tag>
          </Col>
        </Row>
        <Row>
          <Col span={6}>子任务进度:</Col>
          <Col span={10}>
            <Progress percent={(item.current_step / item.total_step) * 100} status={'active'} />
          </Col>
        </Row>
        <Row>
          <Col span={6}>创建日期:</Col>
          <Col>
            <Tag color={datetimeColorMapper[item.badge_color]}>
              {new Date(Date.parse(item.create_date_time)).toLocaleString()}
            </Tag>
          </Col>
        </Row>
        <Row>
          <Col span={6}>项目描述:</Col>
          <Col span={10}>{item.s_project_description || '无项目说明'}</Col>
        </Row>
      </div>
    ),
    actions: (
      <Dropdown overlay={menu(item.mark, item.status)} placement="bottomLeft" arrow>
        <Button>管理</Button>
      </Dropdown>
    ),
  });

  useEffect(() => {
    projectsRuntime().then((result) => setProjectsRuntimeInfo(result));
    return () => {
      setNerDocs(initProjectData.data);
    };
  }, []);

  useEffect(() => {
    if (transferData.login_name !== '') {
      setNerDocs(transferData.data);
    }
    return () => {};
  }, [transferData]);

  useEffect(() => {
    if (transferData.login_name !== '') {
      setDetailModalVisible(true);
    }
    return () => {};
  }, [nerDocs]);

  return (
    <div>
      <ContainerCard
        runtimeData={projectsRuntimeInfo.creating.map(parserData)}
        headerTitle={'创建中'}
      />
      <Divider />
      <ContainerCard
        runtimeData={projectsRuntimeInfo.running.map(parserData)}
        headerTitle={'运行中'}
      />
      <Divider />
      <ContainerCard
        runtimeData={projectsRuntimeInfo.exited.map(parserData)}
        headerTitle={'休眠中'}
      />
      <Divider />
      <ContainerCard
        runtimeData={projectsRuntimeInfo.deleted.map(parserData)}
        headerTitle={'已删除'}
      />

      <Modal
        title="项目详情"
        visible={detailModalVisible}
        onCancel={() => {
          setDetailModalVisible(false);
          setTransferData(initProjectData);
          setNerDocs(initProjectData.data);
        }}
        width={'50%'}
      >
        <ProjectDetail projectData={transferData} />
      </Modal>
    </div>
  );
};
