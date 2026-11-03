public class Shapes {
    sealed interface Shape permits Circle, Square, Rect {}
    record Circle(int r) implements Shape {}
    record Square(int side) implements Shape {}
    record Rect(int w, int h) implements Shape {}

    static int area(Shape s) {
        if (s instanceof Circle c && c.r() > 0) return 3 * c.r() * c.r();
        if (s instanceof Square q) return q.side() * q.side();
        if (s instanceof Rect r) return r.w() * r.h();
        return -1;
    }

    static String label(int n) {
        return switch (n % 4) {
            case 0 -> "zero";
            case 1 -> {
                String t = "one";
                yield t + n;
            }
            default -> {
                if (n < 0) yield "neg";
                yield "many";
            }
        };
    }

    static final String BANNER = """
        shapes
          v1
        """;

    public static void main(String[] args) {
        Shape[] all = {new Circle(2), new Circle(0), new Square(3), new Rect(2, 5)};
        StringBuilder out = new StringBuilder(BANNER.replace("\n", "|"));
        for (Shape s : all) out.append(area(s)).append(',');
        for (int n : new int[]{0, 1, 5, -3, 6}) out.append(label(n)).append(',');
        System.out.println(out);
    }
}
