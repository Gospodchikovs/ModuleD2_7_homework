# ModuleD2_7_homework
Результат выполнения скрипта содержится в файле output.txt. 
Визуальное отображение модели (в формате .dot) содержится в файле news_graph.dot. 
Скрипт для выполнения с домашним заданием находится в файле homework.py. 
База данных модели db.sqlite3 содержит результат выполнения скрипта. 

Добавлено домашнее задание D3.4.
В результате работы с модулем выполны следующие задания:

1. Сделать новую страничку с адресом /news/, на которой должен выводиться список всех новостей.
Все статьи выведены в виде заголовка, даты и первых 50 символов текста статьи.
Новости должны выводиться в порядке от более свежей до самой старой. Отображается всё по адресу /news/.
2. Сделать отдельную страницу для полной информации о статье /news/<id новости>. На этой странице должна быть вся информация о статье. Название, текст и дата загрузки в формате ДЕНЬ-МЕСЯЦ-ГОД ЧАС:МИНУТЫ.
3. Написать собственный фильтр Censor, который цензурирует нежелательную лексику в названиях и текстах статей.
4. Все новые странички должны быть частью основного шаблона default.html.

Добавлено домашнее задание D4.

В результате выполнения заданий к каждому юниту вы должны реализовать следующие действия:

1. Усовершенствовать ваш новостной портал. Добавить постраничный вывод и отдельную страницу с поиском /search/, чтобы пользователь мог сортировать новости по дате и имени автора.
2. Необходимо иметь возможность создавать новые новости и статьи не только из админки, но и в самом приложении. Для такой возможности необходимо создать модельные формы.
3. Необходимо добавить на сайт с помощью дженериков новые страницы /news/add/, а также /news/<int:pk>/edit/. На этих страницах пользователь может добавить или редактировать новости.
4. Добавьте страницу удаления новостей /news/<int:pk>/delete/. На ней после подтверждения пользователь может удалить страницу с новостью.

Добавлено домашнее задание D5

Необхолимо было реализовать:
1. В классе-представлении редактирования профиля добавить проверку аутентификации.
2. Выполнить необходимые настройки пакета allauth в файле конфигурации.
3. В файле конфигурации определить адрес для перенаправления на страницу входа в систему и адрес перенаправления после успешного входа.
4. Реализовать шаблон с формой входа в систему и выполнить настройку конфигурации URL.
5. Реализовать шаблон страницы регистрации пользователей.
6. Реализовать возможность регистрации через Google-аккаунт.
7. Создать группы common и authors.
8. Реализовать автоматическое добавление новых пользователей в группу common.
9. Создать возможность стать автором (быть добавленным в группу authors).
10. Для группы authors предоставить права создания и редактирования объектов модели Post (новостей и статей).
11. В классах-представлениях добавления и редактирования новостей и статей добавить проверку прав доступа.

Добавлено домашнее задание D6.2.

Усовершенствуйте свой новостной сайт.
1. Добавьте пользователю возможность подписываться на рассылку новостей в какой-либо категории. Для этого:
2. Добавьте поле subscribers (соотношение manytomany), в которое будут записываться пользователи, подписанные на обновления в данной категории.
3. При добавлении новости из этой категории пользователю на email, указанный при регистрации, приходит письмо с HTML-кодом заголовка и первых 50 символов текста статьи.
4. В теме письма должен быть сам заголовок статьи. Текст состоит из вышеуказанного HTML и текста: «Здравствуй, username. Новая статья в твоём любимом разделе!».
5. На самом сайте должна быть возможность пользователю подписаться на категорию (добавьте маленькую кнопку «Подписаться», когда пользователь находится на странице новостей в какой-то категории).
6. Дополнительно кроме подписки на странице Категории реализован механизм Отписки от новостей данной категории

Добавлено домашнее задание D6.3.

Усовершенствуйте свой новостной сайт.
1. Добавьте приветственное письмо, которое отправляется пользователю при регистрации.
2. Содержание и посыл письма остается на ваш выбор, главное —обязательно добавьте ссылку на активацию и укажите в нём имя пользователя!

Добавлено домашнее задание D6.4

Усовершенствуйте свой новостной сайт.
1. При создании новости подписчикам этой категории автоматически отправляется сообщение о пополнении в разделе. Содержание письма остаётся на ваше усмотрение, главное, чтобы в нём была отражена краткая информация о данной новости.
2. Один пользователь не может публиковать более трёх новостей в сутки.
