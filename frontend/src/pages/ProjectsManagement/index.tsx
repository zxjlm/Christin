import styles from './index.less';
import ContainerCardList from '@/components/ContainerCardList/index';
import { PageContainer } from '@ant-design/pro-layout';

export default () => {
  return (
    <PageContainer>
      <div className={styles.container}>
        <ContainerCardList />
      </div>
    </PageContainer>
  );
};
