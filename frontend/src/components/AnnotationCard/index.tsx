import { Card, Space, Spin } from 'antd';
import type { annotationType, labelType } from '@/components/SingleAnnotation';
import SingleAnnotation from '@/components/SingleAnnotation';
import type { BasicAPI } from '@/services/site-data/typings';

export default ({ nerDocs, labels }: { nerDocs: BasicAPI.nerDoc[]; labels: labelType[] }) => {
  if (nerDocs.length === 0) return <Spin size={'large'} />;
  return (
    <Card title={'复核标注结果'}>
      <Space direction="vertical">
        {nerDocs.map((doc: { annotations: annotationType[]; text: string }, list_id: number) => (
          <Card type="inner" key={Math.floor(Math.random() * Math.floor(Number.MAX_SAFE_INTEGER))}>
            <SingleAnnotation
              labels={labels}
              // annotationsDefault={doc.annotations}
              text={doc.text}
              list_id={list_id}
            />
          </Card>
        ))}
      </Space>
    </Card>
  );
};
