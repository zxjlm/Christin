import { Form, Button, AutoComplete } from 'antd';
import { useState } from 'react';
import { executeCypher, extract_path } from '@/utils/neoOperations';

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

export const FindPathFrom = ({ setGraphData }: { setGraphData: (props: {}) => void }) => {
  const [options, setOptions] = useState([{ value: 'Loading' }]);
  // const [nameTypeMapper, setNameTypeMapper] = useState({});
  // const [disabled, setDisabled] = useState(true);

  const onFinish = (values: any) => {
    // let query = `MATCH (A:${nameTypeMapper[values.source]} {s_name: ${values.source} ),(B:${nameTypeMapper[values.target]} {s_name: ${values.target}),p = shortestPath((A)-[:]-(B)) RETURN p`
    const query = `MATCH (A {s_name: '${values.source}'}),(B {s_name: '${values.target}'}),p = shortestPath((A)-[*]-(B)) RETURN p`;
    executeCypher(query).then((result) => {
      const { edges, nodes_1 } = extract_path(result);
      setGraphData({ edges, nodes: nodes_1 });
      sessionStorage.setItem('graph', JSON.stringify({ edges, nodes: nodes_1 }));
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
        setOptions(result.records.map((elem) => ({ value: elem._fields[0] })));
        // result.records.forEach(elem => tmp[elem._fields[0]] = elem.labels[0])
        // console.log('tmp',tmp)
        // setNameTypeMapper(tmp)
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
        <AutoComplete options={options} onFocus={onFocus} filterOption={true} />
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
        <AutoComplete options={options} onFocus={onFocus} filterOption={true} />
      </Form.Item>

      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          确认查找
        </Button>
      </Form.Item>
    </Form>
  );
};
