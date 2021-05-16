import React, {useEffect, useState} from 'react';
import {PageContainer} from '@ant-design/pro-layout';
import {Row, Col} from 'antd';
import Introduction from './WelCome/WebsiteIntro';
import DataStoreIntro from './WelCome/DataStoreIntro';
import ProjectIntro from './WelCome/ProjectIntro';
import {websiteBasicData} from "@/services/site-data/api";


export interface dataItemsState {
  name: string,
  value: number
}

const babelMapper = {
  "user_c": '用户数量',
  "herb_c": '中药',
  "pre_c": '处方',
  "gene_c": '基因',
  "pro_c": '蛋白质',
  "other_c": '其他',
  "total_c": '总计',
}

export default (): React.ReactNode => {

  const [userNumbers, setUserNumbers] = useState(0);
  const [dataItems, setDataItems] = useState<dataItemsState[]>([]);

  useEffect(() => {
    websiteBasicData().then(data => {
      const items: dataItemsState[] = []
      Object.entries(data).forEach(elem => {
        if (elem[0] !== 'user_c') items.push({name: babelMapper[elem[0]], value: elem[1]} as dataItemsState)
      })
      setUserNumbers(data.user_c)
      setDataItems(items)
    });
  }, []);

  return (
    <PageContainer>
      <Row>
        <Col span={8}><Introduction userNumbers={userNumbers}/></Col>
        <Col span={5} offset={1}><DataStoreIntro dataItems={dataItems}/></Col>
        <Col span={4} offset={1}><ProjectIntro/></Col>
      </Row>
    </PageContainer>
  );
};
