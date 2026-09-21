import 'package:flutter/material.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const QimatApp());
}

class AppColors {
  static const bg = Color(0xFFF4EDE4);
  static const card = Color(0xFFFFFCF8);
  static const soft = Color(0xFFF1E6D8);
  static const border = Color(0xFFE4D4C0);
  static const text = Color(0xFF21150E);
  static const muted = Color(0xFF8C7766);
  static const brown = Color(0xFF3A2113);
  static const brown2 = Color(0xFF5B371F);
  static const gold = Color(0xFFB9874E);
  static const goldLight = Color(0xFFE7C99B);
  static const red = Color(0xFFC6463A);
}

class QimatApp extends StatelessWidget {
  const QimatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'قیمت',
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: AppColors.bg,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.brown,
          brightness: Brightness.light,
          primary: AppColors.brown,
          secondary: AppColors.gold,
          surface: AppColors.card,
        ),
        textTheme: const TextTheme(
          headlineLarge: TextStyle(fontWeight: FontWeight.w800, color: AppColors.text),
          headlineMedium: TextStyle(fontWeight: FontWeight.w800, color: AppColors.text),
          titleLarge: TextStyle(fontWeight: FontWeight.w800, color: AppColors.text),
          titleMedium: TextStyle(fontWeight: FontWeight.w700, color: AppColors.text),
          bodyLarge: TextStyle(color: AppColors.text),
          bodyMedium: TextStyle(color: AppColors.text),
        ),
      ),
      home: const QimatShell(),
    );
  }
}

class ItemType {
  ItemType(this.name, this.minimumLabor, this.icon);
  String name;
  double minimumLabor;
  IconData icon;
}

class Accessory {
  Accessory(this.name, this.price, this.icon);
  String name;
  double price;
  IconData icon;
}

class QimatModel extends ChangeNotifier {
  double goldPrice = 9850000;
  double weight = 5.25;
  double laborPercent = 7;
  double profitPercent = 7;
  double taxPercent = 10;
  bool manualGoldPrice = true;
  int selectedType = 0;
  int selectedAccessory = 0;

  final List<ItemType> types = [
    ItemType('گردنبند', 2000000, Icons.emoji_objects_outlined),
    ItemType('دستبند', 1500000, Icons.circle_outlined),
    ItemType('انگشتر', 1000000, Icons.ring_volume_outlined),
    ItemType('گوشواره', 1200000, Icons.join_inner_outlined),
    ItemType('ست', 3000000, Icons.favorite_border_rounded),
    ItemType('پلاک', 1000000, Icons.water_drop_outlined),
    ItemType('زنجیر', 1800000, Icons.link_rounded),
  ];

  final List<Accessory> accessories = [
    Accessory('بدون اکسسوری', 0, Icons.cut_outlined),
    Accessory('سنگ', 700000, Icons.diamond_outlined),
    Accessory('مروارید', 600000, Icons.circle_outlined),
    Accessory('چرم', 1200000, Icons.texture_rounded),
    Accessory('ونکلیف', 1500000, Icons.filter_vintage_outlined),
    Accessory('قفل خاص', 900000, Icons.link_outlined),
    Accessory('آویز', 800000, Icons.water_drop_outlined),
  ];

  double get rawGold => goldPrice * weight;
  double get percentageLabor => rawGold * laborPercent / 100;
  double get minimumLabor => types[selectedType].minimumLabor;
  bool get minimumApplied => percentageLabor < minimumLabor;
  double get finalLabor => minimumApplied ? minimumLabor : percentageLabor;
  double get profit => (rawGold + finalLabor) * profitPercent / 100;
  double get tax => (finalLabor + profit) * taxPercent / 100;
  double get accessoryPrice => accessories[selectedAccessory].price;
  double get finalPrice => rawGold + finalLabor + profit + tax + accessoryPrice;

  void setGoldPrice(double v) { goldPrice = v; notifyListeners(); }
  void setWeight(double v) { weight = v; notifyListeners(); }
  void setLabor(double v) { laborPercent = v; notifyListeners(); }
  void setProfit(double v) { profitPercent = v; notifyListeners(); }
  void setTax(double v) { taxPercent = v; notifyListeners(); }
  void setType(int i) { selectedType = i; notifyListeners(); }
  void setAccessory(int i) { selectedAccessory = i; notifyListeners(); }
  void setGoldMode(bool manual) { manualGoldPrice = manual; notifyListeners(); }

  void addType(ItemType item) { types.add(item); notifyListeners(); }
  void updateType(int index, ItemType item) { types[index] = item; notifyListeners(); }
  void deleteType(int index) {
    if (types.length <= 1) return;
    types.removeAt(index);
    if (selectedType >= types.length) selectedType = 0;
    notifyListeners();
  }

  void addAccessory(Accessory item) { accessories.add(item); notifyListeners(); }
  void updateAccessory(int index, Accessory item) { accessories[index] = item; notifyListeners(); }
  void deleteAccessory(int index) {
    if (accessories.length <= 1) return;
    accessories.removeAt(index);
    if (selectedAccessory >= accessories.length) selectedAccessory = 0;
    notifyListeners();
  }
}

class QimatShell extends StatefulWidget {
  const QimatShell({super.key});

  @override
  State<QimatShell> createState() => _QimatShellState();
}

class _QimatShellState extends State<QimatShell> {
  final model = QimatModel();
  int index = 0;

  @override
  Widget build(BuildContext context) {
    final screens = [
      HomePage(model: model, openSummary: () => _openSummary(context)),
      AccessoriesPage(model: model),
      TypesPage(model: model),
      SettingsPage(model: model),
    ];
    return Scaffold(
      body: SafeArea(child: IndexedStack(index: index, children: screens)),
      bottomNavigationBar: QimatBottomNav(
        index: index,
        onChanged: (i) => setState(() => index = i),
      ),
    );
  }

  void _openSummary(BuildContext context) {
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => SummaryPage(model: model)));
  }
}

class QimatBottomNav extends StatelessWidget {
  const QimatBottomNav({super.key, required this.index, required this.onChanged});
  final int index;
  final ValueChanged<int> onChanged;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: AppColors.card,
        border: Border(top: BorderSide(color: AppColors.border)),
      ),
      child: NavigationBar(
        height: 70,
        elevation: 0,
        backgroundColor: AppColors.card,
        indicatorColor: AppColors.soft,
        selectedIndex: index,
        onDestinationSelected: onChanged,
        labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home_rounded), label: 'خانه'),
          NavigationDestination(icon: Icon(Icons.ring_volume_outlined), label: 'اکسسوری‌ها'),
          NavigationDestination(icon: Icon(Icons.category_outlined), label: 'جنس‌ها'),
          NavigationDestination(icon: Icon(Icons.settings_outlined), label: 'تنظیمات'),
        ],
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key, required this.model, required this.openSummary});
  final QimatModel model;
  final VoidCallback openSummary;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: model,
      builder: (context, _) {
        return SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(18, 12, 18, 24),
          child: Column(
            children: [
              const SizedBox(height: 8),
              const Text('قیمت', style: TextStyle(fontSize: 38, fontWeight: FontWeight.w900, color: AppColors.text)),
              const SizedBox(height: 3),
              const Text('دقت در قیمت، اعتماد در معامله', style: TextStyle(fontSize: 12, color: AppColors.muted)),
              const SizedBox(height: 20),
              LuxuryInputRow(
                icon: Icons.layers_outlined,
                title: 'قیمت طلا',
                value: formatMoney(model.goldPrice),
                suffix: 'تومان',
                onTap: () => showNumberEditor(context, title: 'قیمت طلا', initial: model.goldPrice, onSave: model.setGoldPrice),
              ),
              LuxuryInputRow(
                icon: Icons.category_outlined,
                title: 'نوع جنس',
                value: model.types[model.selectedType].name,
                trailing: Icons.keyboard_arrow_down_rounded,
                onTap: () => _chooseType(context),
              ),
              LuxuryInputRow(
                icon: Icons.scale_outlined,
                title: 'وزن',
                value: trimNumber(model.weight),
                suffix: 'گرم',
                onTap: () => showNumberEditor(context, title: 'وزن', initial: model.weight, decimals: true, onSave: model.setWeight),
              ),
              LuxuryInputRow(
                icon: Icons.percent_rounded,
                title: 'اجرت',
                value: trimNumber(model.laborPercent),
                suffix: 'درصد',
                onTap: () => showNumberEditor(context, title: 'اجرت', initial: model.laborPercent, decimals: true, onSave: model.setLabor),
              ),
              LuxuryInputRow(
                icon: Icons.ring_volume_outlined,
                title: 'اکسسوری',
                value: model.accessories[model.selectedAccessory].name,
                trailing: Icons.keyboard_arrow_down_rounded,
                onTap: () => _chooseAccessory(context),
              ),
              const SizedBox(height: 8),
              InkWell(
                borderRadius: BorderRadius.circular(22),
                onTap: openSummary,
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(vertical: 22, horizontal: 20),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(22),
                    gradient: const LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: [AppColors.brown2, AppColors.brown],
                    ),
                    border: Border.all(color: AppColors.gold, width: 1.25),
                    boxShadow: const [BoxShadow(color: Color(0x22000000), blurRadius: 18, offset: Offset(0, 8))],
                  ),
                  child: Column(
                    children: [
                      const Text('قیمت اعلامی به مشتری', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppColors.goldLight)),
                      const SizedBox(height: 10),
                      Text(formatMoney(model.finalPrice), style: const TextStyle(fontSize: 34, height: 1, fontWeight: FontWeight.w900, color: Color(0xFFFFF1D6))),
                      const SizedBox(height: 8),
                      const Text('تومان', style: TextStyle(fontSize: 13, color: AppColors.goldLight)),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 12),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: AppColors.card, borderRadius: BorderRadius.circular(16), border: Border.all(color: AppColors.border)),
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.info_outline_rounded, size: 18, color: AppColors.muted),
                    SizedBox(width: 8),
                    Flexible(child: Text('اجرت، سود، مالیات و اکسسوری‌ها از تنظیمات محاسبه می‌شوند.', textAlign: TextAlign.center, style: TextStyle(fontSize: 11, color: AppColors.muted))),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Future<void> _chooseType(BuildContext context) async {
    final selected = await showModalBottomSheet<int>(
      context: context,
      backgroundColor: AppColors.card,
      showDragHandle: true,
      builder: (_) => SafeArea(
        child: ListView.builder(
          shrinkWrap: true,
          padding: const EdgeInsets.fromLTRB(10, 0, 10, 16),
          itemCount: model.types.length,
          itemBuilder: (_, i) => ListTile(
            leading: Icon(model.types[i].icon, color: AppColors.gold),
            title: Text(model.types[i].name, textDirection: TextDirection.rtl),
            trailing: i == model.selectedType ? const Icon(Icons.check_rounded, color: AppColors.brown) : null,
            onTap: () => Navigator.pop(context, i),
          ),
        ),
      ),
    );
    if (selected != null) model.setType(selected);
  }

  Future<void> _chooseAccessory(BuildContext context) async {
    final selected = await showModalBottomSheet<int>(
      context: context,
      backgroundColor: AppColors.card,
      showDragHandle: true,
      builder: (_) => SafeArea(
        child: ListView.builder(
          shrinkWrap: true,
          padding: const EdgeInsets.fromLTRB(10, 0, 10, 16),
          itemCount: model.accessories.length,
          itemBuilder: (_, i) => ListTile(
            leading: Icon(model.accessories[i].icon, color: AppColors.gold),
            title: Text(model.accessories[i].name, textDirection: TextDirection.rtl),
            subtitle: Text('${formatMoney(model.accessories[i].price)} تومان', textDirection: TextDirection.rtl),
            trailing: i == model.selectedAccessory ? const Icon(Icons.check_rounded, color: AppColors.brown) : null,
            onTap: () => Navigator.pop(context, i),
          ),
        ),
      ),
    );
    if (selected != null) model.setAccessory(selected);
  }
}

class LuxuryInputRow extends StatelessWidget {
  const LuxuryInputRow({
    super.key,
    required this.icon,
    required this.title,
    required this.value,
    this.suffix,
    this.trailing,
    this.onTap,
  });

  final IconData icon;
  final String title;
  final String value;
  final String? suffix;
  final IconData? trailing;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(18),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(18),
          child: Container(
            constraints: const BoxConstraints(minHeight: 66),
            padding: const EdgeInsets.symmetric(horizontal: 12),
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(18), border: Border.all(color: AppColors.border)),
            child: Row(
              textDirection: TextDirection.rtl,
              children: [
                Container(
                  width: 42,
                  height: 42,
                  decoration: const BoxDecoration(color: AppColors.soft, shape: BoxShape.circle),
                  child: Icon(icon, color: AppColors.brown, size: 22),
                ),
                const SizedBox(width: 10),
                Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800)),
                const Spacer(),
                if (suffix != null) ...[
                  Text(suffix!, style: const TextStyle(fontSize: 12, color: AppColors.muted)),
                  const SizedBox(width: 8),
                ],
                Flexible(child: Text(value, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w900))),
                if (trailing != null) ...[
                  const SizedBox(width: 6),
                  Icon(trailing, size: 22, color: AppColors.text),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class SummaryPage extends StatelessWidget {
  const SummaryPage({super.key, required this.model});
  final QimatModel model;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: qimatAppBar(context, 'خلاصه محاسبه'),
      body: AnimatedBuilder(
        animation: model,
        builder: (_, __) => SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(18, 16, 18, 24),
          child: Column(
            children: [
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 4),
                decoration: luxuryCardDecoration(),
                child: Column(
                  children: [
                    SummaryLine('قیمت طلا (هر گرم)', '${formatMoney(model.goldPrice)} تومان'),
                    SummaryLine('وزن', '${trimNumber(model.weight)} گرم'),
                    SummaryLine('مبلغ طلای خام', '${formatMoney(model.rawGold)} تومان'),
                    SummaryLine('اجرت (${trimNumber(model.laborPercent)}%)', '${formatMoney(model.finalLabor)} تومان'),
                    SummaryLine('سود', '${formatMoney(model.profit)} تومان'),
                    SummaryLine('مالیات', '${formatMoney(model.tax)} تومان'),
                    SummaryLine('اکسسوری', '${formatMoney(model.accessoryPrice)} تومان'),
                    const Divider(color: AppColors.border),
                    SummaryLine('قیمت نهایی', '${formatMoney(model.finalPrice)} تومان', bold: true),
                  ],
                ),
              ),
              const SizedBox(height: 14),
              Container(
                padding: const EdgeInsets.all(13),
                decoration: luxuryCardDecoration(),
                child: Row(
                  textDirection: TextDirection.rtl,
                  children: [
                    const Icon(Icons.info_outline_rounded, size: 20, color: AppColors.muted),
                    const SizedBox(width: 8),
                    Expanded(child: Text(model.minimumApplied ? 'حداقل اجرت این نوع جنس اعمال شده است.' : 'اجرت درصدی از حداقل تعریف‌شده بیشتر است.', textDirection: TextDirection.rtl, style: const TextStyle(fontSize: 12, color: AppColors.muted))),
                  ],
                ),
              ),
              const SizedBox(height: 18),
              BrownButton(text: 'بازگشت به صفحه اصلی', onTap: () => Navigator.pop(context)),
            ],
          ),
        ),
      ),
    );
  }
}

class SummaryLine extends StatelessWidget {
  const SummaryLine(this.title, this.value, {super.key, this.bold = false});
  final String title;
  final String value;
  final bool bold;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 13),
      decoration: const BoxDecoration(border: Border(bottom: BorderSide(color: Color(0x22B9874E)))),
      child: Row(
        textDirection: TextDirection.rtl,
        children: [
          Expanded(child: Text(title, textDirection: TextDirection.rtl, style: TextStyle(fontSize: 13, fontWeight: bold ? FontWeight.w800 : FontWeight.w600))),
          Text(value, textDirection: TextDirection.rtl, style: TextStyle(fontSize: bold ? 18 : 14, fontWeight: bold ? FontWeight.w900 : FontWeight.w700)),
        ],
      ),
    );
  }
}

class TypesPage extends StatefulWidget {
  const TypesPage({super.key, required this.model});
  final QimatModel model;

  @override
  State<TypesPage> createState() => _TypesPageState();
}

class _TypesPageState extends State<TypesPage> {
  String query = '';
  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: widget.model,
      builder: (_, __) {
        final items = widget.model.types.asMap().entries.where((e) => e.value.name.contains(query)).toList();
        return Column(
          children: [
            const TopTitle('مدیریت نوع جنس'),
            SearchBox(hint: 'جستجوی نوع جنس ...', onChanged: (v) => setState(() => query = v)),
            Expanded(
              child: ListView.separated(
                padding: const EdgeInsets.fromLTRB(18, 8, 18, 12),
                itemCount: items.length,
                separatorBuilder: (_, __) => const SizedBox(height: 8),
                itemBuilder: (_, i) {
                  final index = items[i].key;
                  final item = items[i].value;
                  return ManageRow(
                    icon: item.icon,
                    title: item.name,
                    onEdit: () => Navigator.push(context, MaterialPageRoute(builder: (_) => EditTypePage(model: widget.model, index: index))),
                    onDelete: () => widget.model.deleteType(index),
                  );
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(18, 0, 18, 14),
              child: BrownButton(
                text: '+ افزودن نوع جنس',
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => EditTypePage(model: widget.model))),
              ),
            ),
          ],
        );
      },
    );
  }
}

class AccessoriesPage extends StatefulWidget {
  const AccessoriesPage({super.key, required this.model});
  final QimatModel model;

  @override
  State<AccessoriesPage> createState() => _AccessoriesPageState();
}

class _AccessoriesPageState extends State<AccessoriesPage> {
  String query = '';
  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: widget.model,
      builder: (_, __) {
        final items = widget.model.accessories.asMap().entries.where((e) => e.value.name.contains(query)).toList();
        return Column(
          children: [
            const TopTitle('مدیریت اکسسوری‌ها'),
            SearchBox(hint: 'جستجوی اکسسوری ...', onChanged: (v) => setState(() => query = v)),
            Expanded(
              child: ListView.separated(
                padding: const EdgeInsets.fromLTRB(18, 8, 18, 12),
                itemCount: items.length,
                separatorBuilder: (_, __) => const SizedBox(height: 8),
                itemBuilder: (_, i) {
                  final index = items[i].key;
                  final item = items[i].value;
                  return ManageRow(
                    icon: item.icon,
                    title: item.name,
                    subtitle: '${formatMoney(item.price)} تومان',
                    onEdit: () => Navigator.push(context, MaterialPageRoute(builder: (_) => EditAccessoryPage(model: widget.model, index: index))),
                    onDelete: () => widget.model.deleteAccessory(index),
                  );
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(18, 0, 18, 14),
              child: BrownButton(
                text: '+ افزودن اکسسوری',
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => EditAccessoryPage(model: widget.model))),
              ),
            ),
          ],
        );
      },
    );
  }
}

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key, required this.model});
  final QimatModel model;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: model,
      builder: (_, __) => SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(18, 0, 18, 24),
        child: Column(
          children: [
            const TopTitle('تنظیمات'),
            SettingTile(
              icon: Icons.percent_rounded,
              title: 'سود پیش‌فرض',
              value: '${trimNumber(model.profitPercent)} درصد',
              onTap: () => showNumberEditor(context, title: 'درصد سود', initial: model.profitPercent, decimals: true, onSave: model.setProfit),
            ),
            SettingTile(
              icon: Icons.receipt_long_outlined,
              title: 'مالیات بر ارزش افزوده',
              value: '${trimNumber(model.taxPercent)} درصد',
              onTap: () => showNumberEditor(context, title: 'درصد مالیات', initial: model.taxPercent, decimals: true, onSave: model.setTax),
            ),
            Container(
              margin: const EdgeInsets.only(bottom: 10),
              padding: const EdgeInsets.all(14),
              decoration: luxuryCardDecoration(),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Row(textDirection: TextDirection.rtl, children: [Icon(Icons.paid_outlined, color: AppColors.brown), SizedBox(width: 10), Text('نحوه قیمت طلا', style: TextStyle(fontWeight: FontWeight.w800))]),
                  const SizedBox(height: 12),
                  RadioListTile<bool>(
                    contentPadding: EdgeInsets.zero,
                    dense: true,
                    value: true,
                    groupValue: model.manualGoldPrice,
                    onChanged: (v) => model.setGoldMode(v ?? true),
                    title: const Text('ورود دستی', textDirection: TextDirection.rtl),
                  ),
                  RadioListTile<bool>(
                    contentPadding: EdgeInsets.zero,
                    dense: true,
                    value: false,
                    groupValue: model.manualGoldPrice,
                    onChanged: (v) => model.setGoldMode(v ?? false),
                    title: const Text('قیمت آنلاین + مبلغ', textDirection: TextDirection.rtl),
                  ),
                ],
              ),
            ),
            const SettingTile(icon: Icons.currency_exchange_rounded, title: 'واحد پول', value: 'تومان'),
            const SettingTile(icon: Icons.format_list_numbered_rounded, title: 'قالب اعداد', value: '۳,۴۵۰,۰۰۰'),
            SettingTile(icon: Icons.support_agent_rounded, title: 'پشتیبانی / بازیابی', value: '', onTap: () {}),
            SettingTile(icon: Icons.info_outline_rounded, title: 'درباره برنامه', value: 'نسخه 0.2.0', onTap: () {}),
          ],
        ),
      ),
    );
  }
}

class TopTitle extends StatelessWidget {
  const TopTitle(this.title, {super.key});
  final String title;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(18, 22, 18, 12),
      child: Center(child: Text(title, textDirection: TextDirection.rtl, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900))),
    );
  }
}

class SearchBox extends StatelessWidget {
  const SearchBox({super.key, required this.hint, required this.onChanged});
  final String hint;
  final ValueChanged<String> onChanged;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(18, 0, 18, 10),
      child: TextField(
        onChanged: onChanged,
        textDirection: TextDirection.rtl,
        decoration: InputDecoration(
          filled: true,
          fillColor: AppColors.card,
          hintText: hint,
          hintTextDirection: TextDirection.rtl,
          prefixIcon: const Icon(Icons.search_rounded, color: AppColors.muted),
          contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: AppColors.border)),
          focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: AppColors.gold)),
        ),
      ),
    );
  }
}

class ManageRow extends StatelessWidget {
  const ManageRow({super.key, required this.icon, required this.title, this.subtitle, required this.onEdit, required this.onDelete});
  final IconData icon;
  final String title;
  final String? subtitle;
  final VoidCallback onEdit;
  final VoidCallback onDelete;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: luxuryCardDecoration(),
      child: Row(
        textDirection: TextDirection.rtl,
        children: [
          Icon(icon, size: 27, color: AppColors.gold),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(title, textDirection: TextDirection.rtl, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800)),
                if (subtitle != null) Text(subtitle!, textDirection: TextDirection.rtl, style: const TextStyle(fontSize: 11, color: AppColors.muted)),
              ],
            ),
          ),
          IconButton(onPressed: onEdit, icon: const Icon(Icons.edit_outlined, size: 20, color: AppColors.brown)),
          IconButton(onPressed: onDelete, icon: const Icon(Icons.delete_outline_rounded, size: 20, color: AppColors.red)),
        ],
      ),
    );
  }
}

class SettingTile extends StatelessWidget {
  const SettingTile({super.key, required this.icon, required this.title, required this.value, this.onTap});
  final IconData icon;
  final String title;
  final String value;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(16),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(16),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 13),
            decoration: luxuryCardDecoration(),
            child: Row(
              textDirection: TextDirection.rtl,
              children: [
                Icon(icon, color: AppColors.brown, size: 22),
                const SizedBox(width: 10),
                Expanded(child: Text(title, textDirection: TextDirection.rtl, style: const TextStyle(fontWeight: FontWeight.w700))),
                if (value.isNotEmpty) Text(value, textDirection: TextDirection.rtl, style: const TextStyle(color: AppColors.muted, fontWeight: FontWeight.w600)),
                if (onTap != null) const SizedBox(width: 6),
                if (onTap != null) const Icon(Icons.chevron_left_rounded, color: AppColors.muted),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class EditTypePage extends StatefulWidget {
  const EditTypePage({super.key, required this.model, this.index});
  final QimatModel model;
  final int? index;
  @override
  State<EditTypePage> createState() => _EditTypePageState();
}

class _EditTypePageState extends State<EditTypePage> {
  late final TextEditingController name;
  late final TextEditingController minLabor;
  IconData icon = Icons.emoji_objects_outlined;

  @override
  void initState() {
    super.initState();
    if (widget.index != null) {
      final item = widget.model.types[widget.index!];
      name = TextEditingController(text: item.name);
      minLabor = TextEditingController(text: formatMoney(item.minimumLabor));
      icon = item.icon;
    } else {
      name = TextEditingController();
      minLabor = TextEditingController(text: '0');
    }
  }

  @override
  Widget build(BuildContext context) {
    final editing = widget.index != null;
    return Scaffold(
      appBar: qimatAppBar(context, editing ? 'ویرایش نوع جنس' : 'افزودن نوع جنس'),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18),
        child: Column(
          children: [
            EditorCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  FieldLabel('نام نوع جنس'),
                  QimatTextField(controller: name, hint: 'مثلاً گردنبند'),
                  const SizedBox(height: 18),
                  FieldLabel('حداقل اجرت'),
                  QimatTextField(controller: minLabor, hint: '0', keyboardType: TextInputType.number),
                  const SizedBox(height: 18),
                  const FieldLabel('آیکون'),
                  IconPicker(current: icon, onChanged: (i) => setState(() => icon = i)),
                ],
              ),
            ),
            const SizedBox(height: 18),
            BrownButton(text: 'ذخیره تغییرات', onTap: _save),
            if (editing) ...[
              const SizedBox(height: 10),
              OutlinedButton(
                style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(52), side: const BorderSide(color: AppColors.gold), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15))),
                onPressed: () { widget.model.deleteType(widget.index!); Navigator.pop(context); },
                child: const Text('حذف', style: TextStyle(color: AppColors.brown, fontWeight: FontWeight.w700)),
              ),
            ],
          ],
        ),
      ),
    );
  }

  void _save() {
    final n = name.text.trim();
    if (n.isEmpty) return;
    final v = parseNumber(minLabor.text);
    final item = ItemType(n, v, icon);
    if (widget.index == null) widget.model.addType(item); else widget.model.updateType(widget.index!, item);
    Navigator.pop(context);
  }
}

class EditAccessoryPage extends StatefulWidget {
  const EditAccessoryPage({super.key, required this.model, this.index});
  final QimatModel model;
  final int? index;
  @override
  State<EditAccessoryPage> createState() => _EditAccessoryPageState();
}

class _EditAccessoryPageState extends State<EditAccessoryPage> {
  late final TextEditingController name;
  late final TextEditingController price;
  IconData icon = Icons.diamond_outlined;

  @override
  void initState() {
    super.initState();
    if (widget.index != null) {
      final item = widget.model.accessories[widget.index!];
      name = TextEditingController(text: item.name);
      price = TextEditingController(text: formatMoney(item.price));
      icon = item.icon;
    } else {
      name = TextEditingController();
      price = TextEditingController(text: '0');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: qimatAppBar(context, widget.index == null ? 'افزودن اکسسوری' : 'ویرایش اکسسوری'),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18),
        child: Column(
          children: [
            EditorCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const FieldLabel('نام اکسسوری'),
                  QimatTextField(controller: name, hint: 'مثلاً سنگ سبز'),
                  const SizedBox(height: 18),
                  const FieldLabel('قیمت'),
                  QimatTextField(controller: price, hint: '0', keyboardType: TextInputType.number),
                  const SizedBox(height: 18),
                  const FieldLabel('آیکون'),
                  IconPicker(current: icon, onChanged: (i) => setState(() => icon = i)),
                ],
              ),
            ),
            const SizedBox(height: 18),
            BrownButton(text: 'ذخیره', onTap: _save),
          ],
        ),
      ),
    );
  }

  void _save() {
    final n = name.text.trim();
    if (n.isEmpty) return;
    final v = parseNumber(price.text);
    final item = Accessory(n, v, icon);
    if (widget.index == null) widget.model.addAccessory(item); else widget.model.updateAccessory(widget.index!, item);
    Navigator.pop(context);
  }
}

class EditorCard extends StatelessWidget {
  const EditorCard({super.key, required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) => Container(width: double.infinity, padding: const EdgeInsets.all(18), decoration: luxuryCardDecoration(), child: child);
}

class FieldLabel extends StatelessWidget {
  const FieldLabel(this.text, {super.key});
  final String text;
  @override
  Widget build(BuildContext context) => Padding(padding: const EdgeInsets.only(bottom: 8), child: Text(text, textDirection: TextDirection.rtl, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700)));
}

class QimatTextField extends StatelessWidget {
  const QimatTextField({super.key, required this.controller, required this.hint, this.keyboardType});
  final TextEditingController controller;
  final String hint;
  final TextInputType? keyboardType;
  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      keyboardType: keyboardType,
      textDirection: TextDirection.rtl,
      decoration: InputDecoration(
        filled: true,
        fillColor: AppColors.card,
        hintText: hint,
        hintTextDirection: TextDirection.rtl,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: AppColors.border)),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: AppColors.border)),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: AppColors.gold)),
      ),
    );
  }
}

class IconPicker extends StatelessWidget {
  const IconPicker({super.key, required this.current, required this.onChanged});
  final IconData current;
  final ValueChanged<IconData> onChanged;
  static const icons = [Icons.emoji_objects_outlined, Icons.ring_volume_outlined, Icons.diamond_outlined, Icons.favorite_border_rounded, Icons.link_rounded, Icons.water_drop_outlined, Icons.circle_outlined, Icons.filter_vintage_outlined];
  @override
  Widget build(BuildContext context) {
    return Wrap(
      alignment: WrapAlignment.end,
      spacing: 8,
      runSpacing: 8,
      children: icons.map((i) => InkWell(
        onTap: () => onChanged(i),
        borderRadius: BorderRadius.circular(14),
        child: Container(
          width: 54,
          height: 54,
          decoration: BoxDecoration(color: i == current ? AppColors.soft : AppColors.card, borderRadius: BorderRadius.circular(14), border: Border.all(color: i == current ? AppColors.gold : AppColors.border)),
          child: Icon(i, color: AppColors.brown),
        ),
      )).toList(),
    );
  }
}

class BrownButton extends StatelessWidget {
  const BrownButton({super.key, required this.text, required this.onTap});
  final String text;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    return FilledButton(
      style: FilledButton.styleFrom(
        minimumSize: const Size.fromHeight(52),
        backgroundColor: AppColors.brown2,
        foregroundColor: const Color(0xFFFFF0D8),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      ),
      onPressed: onTap,
      child: Text(text, textDirection: TextDirection.rtl, style: const TextStyle(fontWeight: FontWeight.w800)),
    );
  }
}

PreferredSizeWidget qimatAppBar(BuildContext context, String title) {
  return AppBar(
    backgroundColor: AppColors.bg,
    elevation: 0,
    centerTitle: true,
    title: Text(title, textDirection: TextDirection.rtl, style: const TextStyle(fontWeight: FontWeight.w900)),
    leading: IconButton(icon: const Icon(Icons.arrow_back_ios_new_rounded, size: 20), onPressed: () => Navigator.maybePop(context)),
  );
}

BoxDecoration luxuryCardDecoration() => BoxDecoration(
  color: AppColors.card,
  borderRadius: BorderRadius.circular(16),
  border: Border.all(color: AppColors.border),
  boxShadow: const [BoxShadow(color: Color(0x0F000000), blurRadius: 12, offset: Offset(0, 5))],
);

Future<void> showNumberEditor(
  BuildContext context, {
  required String title,
  required double initial,
  required ValueChanged<double> onSave,
  bool decimals = false,
}) async {
  final controller = TextEditingController(text: decimals ? trimNumber(initial) : formatMoney(initial));
  final result = await showModalBottomSheet<double>(
    context: context,
    isScrollControlled: true,
    backgroundColor: AppColors.card,
    showDragHandle: true,
    builder: (context) => Padding(
      padding: EdgeInsets.fromLTRB(18, 8, 18, MediaQuery.of(context).viewInsets.bottom + 18),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(title, textDirection: TextDirection.rtl, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900)),
          const SizedBox(height: 12),
          QimatTextField(controller: controller, hint: '0', keyboardType: const TextInputType.numberWithOptions(decimal: true)),
          const SizedBox(height: 14),
          BrownButton(text: 'ثبت', onTap: () => Navigator.pop(context, parseNumber(controller.text))),
        ],
      ),
    ),
  );
  if (result != null) onSave(result);
}

String formatMoney(double value) {
  final s = value.round().toString();
  final buffer = StringBuffer();
  for (int i = 0; i < s.length; i++) {
    final position = s.length - i;
    buffer.write(s[i]);
    if (position > 1 && position % 3 == 1) buffer.write(',');
  }
  return buffer.toString();
}

String trimNumber(double value) {
  if (value == value.roundToDouble()) return value.toInt().toString();
  return value.toStringAsFixed(2).replaceFirst(RegExp(r'0+$'), '').replaceFirst(RegExp(r'\.$'), '');
}

double parseNumber(String text) {
  final cleaned = text.replaceAll(',', '').replaceAll('٫', '.').replaceAll(RegExp(r'[^0-9.]'), '');
  return double.tryParse(cleaned) ?? 0;
}
