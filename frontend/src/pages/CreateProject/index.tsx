import { useState } from 'react';
import NormalStepFrom from '@/components/InputStepForms/NormalStepForm';
import ProCard from '@ant-design/pro-card';
import StructStepForm from '@/components/InputStepForms/StructStepForm';
import HalfStructStepFrom from '@/components/InputStepForms/HalfStructStepForm';

export default () => {
  const [tab, setTab] = useState('tab1');

  return (
    <div>
      <ProCard
        tabs={{
          tabPosition: 'left',
          activeKey: tab,
          onChange: (key) => {
            setTab(key);
          },
        }}
      >
        <ProCard.TabPane key="tab1" tab="结构化数据">
          <StructStepForm />
        </ProCard.TabPane>
        <ProCard.TabPane key="tab2" tab="半结构化数据">
          <HalfStructStepFrom />
        </ProCard.TabPane>
        <ProCard.TabPane key="tab3" tab="非结构化数据">
          <NormalStepFrom />
        </ProCard.TabPane>
      </ProCard>
    </div>
  );
};
