import {Form, Button, AutoComplete, Switch} from 'antd';
import {useState} from 'react';
import {executeCypher, neoQuery} from '@/utils/neoOperations';

const layout = {
  labelCol: {
    span: 5,
  },
  wrapperCol: {
    span: 16,
  },
};
const tailLayout = {
  wrapperCol: {
    offset: 5,
    span: 16,
  },
};

export const FindPathFrom = ({setGraphData}: { setGraphData: (x: any) => void }) => {
  const [options, setOptions] = useState([{value: 'Loading'}]);
  // const [nameTypeMapper, setNameTypeMapper] = useState({});
  // const [disabled, setDisabled] = useState(true);

  const onFinish = (values: any) => {
    const pathType = values.path_type ? 'shortestPath' : 'allShortestPaths'
    const query = `MATCH (A {s_name: '${values.source}'}),(B {s_name: '${values.target}'}),p = ${pathType}((A)-[*]-(B)) RETURN p`;
    neoQuery(query).then((result) => {

      setGraphData(result);
      sessionStorage.setItem('graph', JSON.stringify(result));
    });
  };

  const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
  };

  const onFocus = () => {
    if (options[0].value === 'Loading') {
      executeCypher('MATCH (n) RETURN n.s_name').then((result) => {
        // @ts-ignore
        // eslint-disable-next-line no-underscore-dangle
        setOptions(result.records.map((elem) => ({value: elem._fields[0]})));
      });
    }
  };

  return (
    <Form {...layout} name="find-path" onFinish={onFinish} onFinishFailed={onFinishFailed}>
      <Form.Item
        label="起点"
        name="source"
        rules={[
          {
            required: true,
            message: 'Please input source!',
          },
        ]}
      >
        <AutoComplete options={options} onFocus={onFocus} filterOption={true}/>
      </Form.Item>

      <Form.Item
        label="终点"
        name="target"
        rules={[
          {
            required: true,
            message: 'Please input target!',
          },
        ]}
      >
        <AutoComplete options={options} onFocus={onFocus} filterOption={true}/>
      </Form.Item>

      <Form.Item
        label="路径类型"
        name="path_type"
        initialValue={true}
      >
        <Switch
          checkedChildren={'查找单条路径'}
          unCheckedChildren={'查找所有路径'}
          defaultChecked={true}
          // onChange={(checked) => setNeedEmail(checked)}
        />
      </Form.Item>

      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          确认查找
        </Button>
      </Form.Item>
    </Form>
  );
};
