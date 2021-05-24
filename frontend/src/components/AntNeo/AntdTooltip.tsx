import { Card, Typography } from 'antd';
import React from 'react';
import { GraphinContext } from '@antv/graphin';
import { hashCode } from '@/utils/useful';

const CustomContextMenu = (props: { content: any }) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { content } = props;
  const nodeSize = 40;

  const generate_card = () => {
    const banItem = ['layout', 'queryId', 'style', 'x', 'y', 'degree', 'type'];
    const ret = [];
    // eslint-disable-next-line no-restricted-syntax
    for (const contentKey in content) {
      if (
        banItem.findIndex((e) => e === contentKey) === -1 &&
        content.hasOwnProperty(contentKey) &&
        contentKey[0] !== '_'
      ) {
        ret.push(`${contentKey}:${content[contentKey]}`);
      }
    }
    return ret;
  };

  return (
    <div
      style={{
        position: 'absolute',
        left: 200, // x,
        top: nodeSize, // y,
      }}
    >
      <Card title={content.s_name}>
        <Typography>
          <ul>
            {generate_card().slice(0,3).map((e) => (
              <li key={hashCode(e)}>{e}</li>
            ))}
            <li key={'props-tips'}>... (右击节点可以查看更多信息)</li>
          </ul>
        </Typography>{' '}
      </Card>
    </div>
  );
};

export const AntdTooltip = () => {
  const { tooltip } = React.useContext(GraphinContext);
  const context = tooltip.node;
  const { item } = context;
  const model = item && item.getModel();
  return (
    // @ts-ignore
    <div>
      <CustomContextMenu content={model} />
    </div>
  );
};
