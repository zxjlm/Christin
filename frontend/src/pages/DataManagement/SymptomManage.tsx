import TableDataManagement from '@/components/TableDataManagement'
import {PageHeaderWrapper} from "@ant-design/pro-layout";
import {Card, Tabs} from "antd";

const {TabPane} = Tabs

export default () => {
  return <PageHeaderWrapper>
    <Tabs defaultActiveKey="1">
      <TabPane tab="MMSymptom" key="1">
        <Card>
          <TableDataManagement modelName='MMSymptom'/>
        </Card>
      </TabPane>
      <TabPane tab="TCMSymptom" key="2">
        <Card>
          <TableDataManagement modelName='TCMSymptom'/>
        </Card>
      </TabPane>
    </Tabs>

  </PageHeaderWrapper>
}
