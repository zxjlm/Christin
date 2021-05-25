export default [
  {
    path: '/user',
    layout: false,
    routes: [
      {
        path: '/user',
        routes: [
          {
            name: 'login',
            path: '/user/login',
            component: './user/Login',
          },
        ],
      },
    ],
  },
  {
    path: '/graphinneo',
    layout: false,
    routes: [
      {
        path: '/graphinneo',
        routes: [
          {
            name: 'graph',
            path: '/graphinneo/graph/:port/:pwd',
            component: './AntNeo/index',
          },
        ],
      },
    ],
  },
  {
    path: '/welcome',
    name: 'welcome',
    icon: 'smile',
    component: './Welcome',
  },
  {
    path: '/project-management',
    name: 'project-management',
    icon: 'smile',
    component: './ProjectsManagement/index',
  },
  {
    path: '/create-project',
    name: 'create-project',
    icon: 'smile',
    component: './CreateProject/index',
  },
  {
    path: '/data-management',
    name: 'data-management',
    icon: 'crown',
    access: 'canAdmin',
    // component: './DataManagement',
    routes: [
      {
        path: '/data-management/herb-manage',
        name: 'herb-manage',
        icon: 'smile',
        component: './DataManagement/HerbManage',
      },
      {
        path: '/data-management/ingredient-manage',
        name: 'ingredient-manage',
        icon: 'smile',
        component: './DataManagement/IngredientManage',
      },
      {
        path: '/data-management/target-manage',
        name: 'target-manage',
        icon: 'smile',
        component: './DataManagement/TargetManage',
      },
      {
        path: '/data-management/symptom-manage',
        name: 'symptom-manage',
        icon: 'smile',
        component: './DataManagement/SymptomManage',
      },
      {
        path: '/data-management/disease-manage',
        name: 'disease-manage',
        icon: 'smile',
        component: './DataManagement/DiseaseManage',
      },
    ],
  },
  // {
  //   name: 'list.table-list',
  //   icon: 'table',
  //   path: '/list',
  //   component: './TableList',
  // },
  {
    path: '/',
    redirect: '/welcome',
  },
  {
    component: './404',
  },
];
