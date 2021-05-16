import { PageHeader } from 'antd';
import { DynamicLayout } from '@/components/AntNeo/DynamicLayout';
import { useEffect } from 'react';

export default (props: any) => {
  useEffect(() => {
    return () => {
      localStorage.setItem('neo-port', '-1');
      localStorage.setItem('neo-pwd', 'undefined');
    };
  }, []);

  return (
    <div>
      <PageHeader title={'Christin Graph'} />
      <main>
        <DynamicLayout port={props.match.params.port} pwd={props.match.params.pwd} />
      </main>
    </div>
  );
};
